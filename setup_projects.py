#!/usr/bin/env python3
"""
JIRA Project Setup Script
Ensures that required JIRA projects exist before creating issues.
"""

from env_loader import load_env
from jira_client import JiraClient
import time
import sys

class ProjectSetup:
    def __init__(self):
        env = load_env()
        self.jira = JiraClient(
            env["JIRA_SERVER"], 
            env["JIRA_EMAIL"], 
            env["JIRA_API_TOKEN"],
            env.get("JIRA_PROJECT_KEY")
        )
        
        # Projects to be created for the proof of concept
        self.projects_to_create = [
            {
                "key": "DEVOPS",
                "name": "DevOps and Infrastructure",
                "description": "Project for infrastructure, CI/CD, and operations tickets"
            },
            {
                "key": "WEBAPP",
                "name": "Web Application",
                "description": "Development and maintenance of the main web application"
            },
            {
                "key": "SUPPORT",
                "name": "Technical Support", 
                "description": "User support and technical inquiry tickets"
            },
            {
                "key": "SECURITY",
                "name": "Security",
                "description": "Vulnerabilities, audits, and security improvements"
            },
            {
                "key": "DOCS",
                "name": "Documentation",
                "description": "Creation and maintenance of technical documentation"
            }
        ]
    
    def cleanup_and_recreate(self):
        """Delete existing projects and recreate them with Kanban boards"""
        print("🧹 JIRA Project Setup - Cleanup and Recreation with Kanban")
        print("=" * 60)
        
        # Check connection
        if not self.jira.test_connection():
            print("❌ Error: Unable to connect to JIRA")
            return False
        
        print("✅ Successfully connected to JIRA")
        
        # Get existing projects
        print("\n📋 Fetching existing projects...")
        try:
            existing_projects = self.jira.get_all_projects()
            # Include only relevant projects for cleanup
            all_keys = [p["key"] for p in existing_projects]
            cleanup_keys = [key for key in all_keys if key in ["TEST", "SCRUM"] + [config["key"] for config in self.projects_to_create]]
            
            print(f"📂 Projects to be deleted: {cleanup_keys if cleanup_keys else 'None'}")
            
        except Exception as e:
            print(f"⚠️ Error fetching projects: {e}")
            cleanup_keys = []
        
        # Phase 1: Delete existing projects
        if cleanup_keys:
            print(f"\n🗑️  Deleting {len(cleanup_keys)} existing projects...")
            print("-" * 60)
            
            for project_key in cleanup_keys:
                try:
                    print(f"🔥 Deleting project: {project_key}")
                    self.jira.delete_project(project_key)
                    print(f"✅ Project {project_key} deleted")
                    time.sleep(2)  # Pause between deletions
                except Exception as e:
                    print(f"❌ Error deleting {project_key}: {e}")
                    continue
            
            print(f"\n⏱️  Waiting 10 seconds for JIRA to process deletions...")
            time.sleep(10)
        
        # Phase 2: Create new projects
        print(f"\n🏗️  Creating {len(self.projects_to_create)} projects with Kanban boards...")
        print("-" * 60)
        
        created_projects = []
        failed_projects = []
        
        for project_config in self.projects_to_create:
            project_key = project_config["key"]
            project_name = project_config["name"]
            
            print(f"\n📁 Creating Kanban project: {project_key} - {project_name}")
            
            try:
                result = self.jira.create_project(
                    key=project_config["key"],
                    name=project_config["name"],
                    description=project_config["description"]
                )
                
                created_projects.append(project_key)
                print(f"✅ Project {project_key} created with Kanban board")
                print(f"   🔗 URL: {result.get('self', 'N/A')}")
                
                time.sleep(3)  # Avoid API rate limiting
                
            except Exception as e:
                failed_projects.append(project_key)
                print(f"❌ Error creating project {project_key}: {e}")
                continue
        
        # Final summary
        print("\n" + "="*60)
        print("📊 KANBAN PROJECT SETUP SUMMARY")
        print("="*60)
        print(f"🗑️  Projects deleted: {len(cleanup_keys)}")
        for key in cleanup_keys:
            print(f"   • {key}")
            
        print(f"\n✅ Projects created with Kanban: {len(created_projects)}")
        for key in created_projects:
            print(f"   • {key}")
            
        print(f"\n❌ Projects failed to create: {len(failed_projects)}")
        for key in failed_projects:
            print(f"   • {key}")
        
        if len(created_projects) > 0:
            print(f"\n🎉 Setup complete! Kanban projects ready.")
            print(f"💡 Features of the new projects:")
            print(f"   📋 Pre-configured Kanban boards")
            print(f"   🔄 Workflow: To Do → In Progress → Done")
            print(f"   🏷️  Ready for automatic label classification")
            print(f"\n📝 Next steps:")
            print(f"   python seeder.py    # Create issues in Kanban boards")
            print(f"   python main.py      # Classify and tag issues")
            return True
        else:
            print(f"\n⚠️ No projects could be created. Please review the errors.")
            return False
    
    def list_projects(self):
        """List all available projects"""
        print("📋 Available JIRA Projects:")
        print("-" * 40)
        
        try:
            projects = self.jira.get_all_projects()
            if not projects:
                print("No projects configured")
                return
                
            for project in projects:
                print(f"🔹 {project['key']} - {project['name']}")
                print(f"   📝 {project.get('description', 'No description')}")
                print(f"   🔗 {project.get('self', '')}")
                print()
                
        except Exception as e:
            print(f"❌ Error fetching projects: {e}")

def main():
    print("🎯 JIRA Project Setup")
    print("Automated project setup with Kanban boards")
    print()
    
    setup = ProjectSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        setup.list_projects()
        return
    
    # Cleanup warning
    print("⚠️  This process will delete existing projects and recreate them with Kanban boards")
    print("📋 Projects included: DEVOPS, WEBAPP, SUPPORT, SECURITY, DOCS, TEST, SCRUM")
    print()
    
    success = setup.cleanup_and_recreate()
    
    if not success:
        print(f"\n❌ Setup failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
