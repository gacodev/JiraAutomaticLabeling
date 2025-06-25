import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import logging

class JiraClient:
    def __init__(self, server, email, token, project_key=None):
        self.server = server
        self.email = email
        self.token = token
        self.project_key = project_key
        # Use Basic Auth with email + API token (works!)
        self.auth = HTTPBasicAuth(email, token)
        self.headers = {
            "Accept": "application/json", 
            "Content-Type": "application/json"
        }
        
    def test_connection(self):
        try:
            # Use a reliable endpoint to verify connectivity
            url = f"{self.server}/rest/api/3/permissions"
            response = requests.get(url, headers=self.headers, auth=self.auth, timeout=10)
            
            if response.status_code == 200:
                return True
            else:
                logging.error(f"JIRA response: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Error connecting to JIRA: {e}")
            return False

    def get_all_tickets(self):
        start_at = 0
        max_results = 50
        all_issues = []
        
        while True:
            jql = f'project = "{self.project_key}"' if self.project_key else "order by created DESC"
            params = {
                "jql": jql, 
                "fields": ["summary", "description", "labels", "issuetype", "status", "created"],
                "maxResults": max_results,
                "startAt": start_at
            }
            
            url = f"{self.server}/rest/api/3/search"
            response = requests.get(url, params=params, headers=self.headers, auth=self.auth)
            response.raise_for_status()
            
            data = response.json()
            issues = data["issues"]
            all_issues.extend(issues)
            
            if len(issues) < max_results:
                break
                
            start_at += max_results
            
        return all_issues

    def get_tickets_updated_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        jql_base = f'updated >= "{today}"'
        
        if self.project_key:
            jql = f'project = "{self.project_key}" AND {jql_base}'
        else:
            jql = jql_base
            
        params = {
            "jql": jql,
            "fields": ["summary", "description", "labels"],
            "maxResults": 100
        }
        url = f"{self.server}/rest/api/3/search"
        response = requests.get(url, params=params, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()["issues"]

    def assign_labels(self, issue_key, labels):
        url = f"{self.server}/rest/api/3/issue/{issue_key}"
        data = {
            "update": {
                "labels": [{"add": label} for label in labels]
            }
        }
        response = requests.put(url, json=data, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        
    def create_ticket(self, summary, description, issue_type="Task"):
        if not self.project_key:
            raise ValueError("project_key is required to create tickets")
            
        url = f"{self.server}/rest/api/3/issue"
        # Atlassian Document Format (ADF) for description field
        adf_description = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": description
                        }
                    ]
                }
            ]
        }
        
        data = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary,
                "description": adf_description,
                "issuetype": {"name": issue_type}
            }
        }
        
        response = requests.post(url, json=data, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()
        
    def create_project(self, key, name, description="Automatically created project", project_type="software"):
        """Create a new JIRA project with Kanban board"""
        # Get current user's accountId to assign as project lead
        my_user = self.get_current_user()
        account_id = my_user["accountId"]
        
        url = f"{self.server}/rest/api/3/project"
        data = {
            "key": key,
            "name": name,
            "description": description,
            "projectTypeKey": project_type,
            "leadAccountId": account_id
        }
        
        response = requests.post(url, json=data, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()
        
    def project_exists(self, project_key):
        """Check if a project exists"""
        try:
            url = f"{self.server}/rest/api/3/project/{project_key}"
            response = requests.get(url, headers=self.headers, auth=self.auth)
            return response.status_code == 200
        except:
            return False
            
    def get_all_projects(self):
        """Retrieve all JIRA projects"""
        url = f"{self.server}/rest/api/3/project"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()
        
    def get_current_user(self):
        """Get information of the current authenticated user"""
        url = f"{self.server}/rest/api/3/myself"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()
        
    def delete_project(self, project_key):
        """Delete a project"""
        url = f"{self.server}/rest/api/3/project/{project_key}"
        response = requests.delete(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return True
        
    def get_project_info(self):
        """Get project information by key"""
        if not self.project_key:
            return None
            
        url = f"{self.server}/rest/api/3/project/{self.project_key}"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()
