from env_loader import load_env
from jira_client import JiraClient
from labels_classifier import TicketClassifier
import sys
import logging

def main():
    print("🤖 JIRA AI Classifier - Automatic Labeling System")
    print("=" * 60)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Load configuration
    try:
        env = load_env()
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        sys.exit(1)
    
    # Initialize clients
    jira = JiraClient(
        env["JIRA_SERVER"], 
        env["JIRA_EMAIL"], 
        env["JIRA_API_TOKEN"],
        env.get("JIRA_PROJECT_KEY")
    )
    classifier = TicketClassifier(model_name="gemma3:latest")
    
    # Test connections
    print("\n🔍 Testing connections...")
    
    if not jira.test_connection():
        print("❌ Error: Unable to connect to JIRA")
        print("Check your credentials in the .env file")
        sys.exit(1)
    print("✅ JIRA: Connection successful")
    
    if not classifier.test_connection():
        print("❌ Error: Unable to connect to Ollama")
        print("Make sure Ollama is running: `ollama serve`")
        print("And that you have the Gemma model: `ollama pull gemma:8b`")
        sys.exit(1)
    print("✅ Ollama: Connection successful")
    
    # Show project info
    if jira.project_key:
        try:
            project_info = jira.get_project_info()
            print(f"📋 Project: {project_info['name']} ({project_info['key']})")
        except Exception as e:
            print(f"⚠️ Could not retrieve project info: {e}")
    
    # Fetch all tickets
    print("\n📚 Fetching ALL tickets from all projects...")
    tickets = jira.get_all_tickets()
    apply_labels = True
    
    if not tickets:
        print("📭 No tickets found to process")
        return
    
    print(f"🎟️ Tickets retrieved: {len(tickets)}")
    
    # Stats
    classified = 0
    errors = 0
    labels_applied = 0
    
    print(f"\n🚀 Starting {'classification and labeling' if apply_labels else 'analysis'}...")
    print("-" * 60)
    
    for i, issue in enumerate(tickets, 1):
        key = issue["key"]
        fields = issue["fields"]
        summary = fields.get("summary", "")
        description = fields.get("description", "")
        current_labels = [label for label in fields.get("labels", [])]
        
        print(f"\n[{i}/{len(tickets)}] 🎫 Processing: {key}")
        print(f"📝 Title: {summary}")
        
        if current_labels:
            print(f"🏷️ Current labels: {current_labels}")
        
        try:
            # Classify ticket
            suggested_labels = classifier.classify(summary, description)
            
            if suggested_labels:
                print(f"🤖 Suggested labels: {suggested_labels}")
                classified += 1
                
                if apply_labels:
                    # Filter out existing labels
                    new_labels = [label for label in suggested_labels if label not in current_labels]
                    
                    if new_labels:
                        jira.assign_labels(key, new_labels)
                        labels_applied += len(new_labels)
                        print(f"✅ Labels applied: {new_labels}")
                    else:
                        print("ℹ️ Labels already existed, no changes applied")
                else:
                    print("🔍 Analysis mode - labels not applied")
            else:
                print("⚠️ Could not determine labels for this ticket")
                errors += 1
                
        except Exception as e:
            print(f"❌ Error processing ticket {key}: {e}")
            errors += 1
            continue
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    print(f"🎟️ Total tickets processed: {len(tickets)}")
    print(f"✅ Successfully classified: {classified}")
    print(f"❌ Classification errors: {errors}")
    
    if apply_labels:
        print(f"🏷️ Total labels applied: {labels_applied}")
        print(f"\n🎉 Automatic classification completed!")
    else:
        print(f"\n🔍 Analysis completed!")
    
    print(f"📈 Success rate: {(classified / len(tickets) * 100):.1f}%")

def show_help():
    print("🤖 JIRA AI Classifier")
    print("Usage: python main.py [options]")
    print("\nOptions:")
    print("  --help     Show this help message")
    print("  --version  Show version info")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if "--help" in sys.argv:
            show_help()
            sys.exit(0)
        elif "--version" in sys.argv:
            print("JIRA AI Classifier v1.0.0")
            sys.exit(0)
    
    main()
