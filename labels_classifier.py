import requests
import json
import logging

class TicketClassifier:
    def __init__(self, model_name="gemma3:latest"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"
        self.valid_labels = [
            "initiative", "maintenance", "cost optimization"
        ]
        
    def test_connection(self):
        try:
            response = requests.post(self.ollama_url, json={
                "model": self.model_name,
                "prompt": "Test",
                "stream": False
            }, timeout=60)
            return response.status_code == 200
        except Exception as e:
            logging.error(f"Error connecting to Ollama: {e}")
            return False

    def classify(self, summary, description):
        if not self.test_connection():
            print("❌ Error: Cannot connect to Ollama")
            return []
            
        prompt = f"""
You are an expert in classifying JIRA tickets. Analyze the ticket title and description and classify it into exactly ONE of the following categories:

AVAILABLE CATEGORIES:
- "maintenance": Maintenance tasks, minor fixes, code cleanup
- "support": Technical support tickets, user help, questions
- "initiative": New features, projects, business initiatives
- "optimization": Performance improvements, optimizations, refactoring
- "documentation": Creating or updating documentation

TICKET TO CLASSIFY:
Title: {summary}
Description: {description or "No description provided"}

INSTRUCTIONS:
1. Select up to 2 most relevant categories
2. Respond ONLY with a valid JSON array
3. Use exactly the category names listed above

REQUIRED RESPONSE FORMAT:
["category1", "category2"]

EXAMPLES:
- Title: "Login not working" → ["maintenance", "support"]
- Title: "Implement new dashboard" → ["initiative"]
- Title: "Update API documentation" → ["documentation"]
- Title: "Optimize database queries" → ["optimization"]
"""

        try:
            response = requests.post(self.ollama_url, json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }, timeout=60)
            response.raise_for_status()
            
            text = response.json()["response"].strip()
            
            # Clean up the response
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].strip()
            
            # Look for JSON array in the response
            if "[" in text and "]" in text:
                start = text.find("[")
                end = text.rfind("]") + 1
                text = text[start:end]
            
            # Safely parse JSON
            labels = json.loads(text)
            
            # Validate the labels are in the accepted list
            valid_labels = [label for label in labels if label in self.valid_labels]
            
            if valid_labels:
                return valid_labels[:2]  # Return a maximum of 2 labels
            else:
                print(f"⚠️ Invalid labels in response: {labels}")
                return []
                
        except json.JSONDecodeError as e:
            print(f"⚠️ Error parsing JSON: {text}")
            return []
        except Exception as e:
            print(f"❌ Error classifying ticket: {e}")
            return []
