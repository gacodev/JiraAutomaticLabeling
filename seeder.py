from env_loader import load_env
from jira_client import JiraClient
import time

class JiraSeeder:
    def __init__(self):
        env = load_env()
        self.jira = JiraClient(
            env["JIRA_SERVER"], 
            env["JIRA_EMAIL"], 
            env["JIRA_API_TOKEN"],
            env.get("JIRA_PROJECT_KEY")
        )
        
    def create_sample_tickets(self):
        """Create sample tickets to test the classifier"""
        
        # Fetch available projects
        try:
            projects = self.jira.get_all_projects()
            if not projects:
                print("❌ No available projects found. Run: python setup_projects.py first.")
                return []
            
            project_keys = [p["key"] for p in projects]
            print(f"📂 Available projects: {project_keys}")
        except Exception as e:
            print(f"❌ Error fetching projects: {e}")
            return []
        
        # Sample tickets with strategic content
        sample_tickets = [
            {
                "summary": "App crashes unexpectedly on login",
                "description": "When users try to log in, the app crashes without any error message. This happens in about 30% of login attempts.",
                "issue_type": "Task"
            },
            {
                "summary": "Implement real-time metrics dashboard",
                "description": "We need a new dashboard showing system metrics in real time: active users, transactions per minute, and service health.",
                "issue_type": "Task"
            },
            {
                "summary": "User can't reset password",
                "description": "Users report they don't receive the password reset email. The button works but no email is delivered. Investigate the email service.",
                "issue_type": "Task"
            },
            {
                "summary": "Configure CI/CD pipeline for new microservice",
                "description": "Set up CI/CD pipeline for the payment microservice, including automated tests, Docker build, and deploy to staging and production.",
                "issue_type": "Task"
            },
            {
                "summary": "Optimize report database queries",
                "description": "Monthly report queries take over 5 minutes. We need to optimize indexes and review slowest queries.",
                "issue_type": "Task"
            },
            {
                "summary": "Update REST API documentation",
                "description": "API documentation is outdated. Update all endpoints, request/response examples, and add new authentication endpoints.",
                "issue_type": "Task"
            },
            {
                "summary": "Implement two-factor authentication",
                "description": "For security, we need to implement 2FA for all admin users. It must support Google Authenticator and SMS.",
                "issue_type": "Task"
            },
            {
                "summary": "Database server running out of space",
                "description": "Production DB is at 95% capacity. We need to purge old logs and increase storage space.",
                "issue_type": "Task"
            },
            {
                "summary": "User reports file upload failure",
                "description": "A specific user can't upload PDF files. Others have no issue. Logs show no obvious errors.",
                "issue_type": "Task"
            },
            {
                "summary": "Migrate application to Kubernetes",
                "description": "Migrate the entire application from physical servers to Kubernetes for better scalability and maintenance.",
                "issue_type": "Task"
            },
            {
                "summary": "Create new live chat feature",
                "description": "Customers have requested a live chat feature for support. It should integrate with the existing ticket system.",
                "issue_type": "Task"
            },
            {
                "summary": "Set up APM monitoring for microservices",
                "description": "Implement Application Performance Monitoring for all microservices using Prometheus and Grafana.",
                "issue_type": "Task"
            },
            {
                "summary": "Reports page loads very slowly",
                "description": "Users complain that the reports page takes over 30 seconds to load. Optimize queries and implement caching.",
                "issue_type": "Task"
            },
            {
                "summary": "Update frontend security libraries",
                "description": "15 security vulnerabilities found by `npm audit`. All dependencies must be updated to safe versions.",
                "issue_type": "Task"
            },
            {
                "summary": "How do I change my profile picture?",
                "description": "A user asks how to change their profile picture. They can't find the option in settings.",
                "issue_type": "Task"
            },
            {
                "summary": "Implement feature flags for new features",
                "description": "We need a feature flag system to toggle features without deployment. Evaluate LaunchDarkly or custom solution.",
                "issue_type": "Task"
            },
            {
                "summary": "Automatic backup has been failing",
                "description": "The backup system hasn’t worked since last Monday. Logs show connection errors with S3 storage.",
                "issue_type": "Task"
            },
            {
                "summary": "Create onboarding guide for new developers",
                "description": "We need complete onboarding documentation: environment setup, system architecture, coding standards, and deployment guide.",
                "issue_type": "Task"
            },
            {
                "summary": "Apply security patches to web server",
                "description": "3 critical CVEs detected on our Apache server. We must apply patches in the next maintenance window.",
                "issue_type": "Task"
            },
            {
                "summary": "Refactor legacy payments module",
                "description": "Legacy payment module (5+ years old) is hard to maintain. We need a complete refactor using modern best practices.",
                "issue_type": "Task"
            },
            {
                "summary": "Set up monitoring alerts for critical metrics",
                "description": "Configure alerts for: CPU > 80%, memory > 90%, disk > 95%, app errors > 5 per minute.",
                "issue_type": "Task"
            },
            {
                "summary": "Implement push notification system",
                "description": "Users want push notifications for important events. Must support both web and mobile (Android/iOS).",
                "issue_type": "Task"
            },
            {
                "summary": "500 error when exporting large reports to Excel",
                "description": "Exporting large reports to Excel triggers a 500 error. Works fine with small reports.",
                "issue_type": "Task"
            },
            {
                "summary": "Set up isolated automated testing environment",
                "description": "Create a dedicated environment for automated testing with mock data and isolated configuration.",
                "issue_type": "Task"
            },
            {
                "summary": "Confirmation emails are not being sent",
                "description": "Users don’t receive confirmation emails after signing up. Registration works, but no email is delivered. Check SMTP service.",
                "issue_type": "Task"
            }
        ]
        
        # Distribute tickets across available projects
        created_tickets = []
        print(f"🚀 Creating {len(sample_tickets)} tickets distributed across {len(project_keys)} projects...")

        for i, ticket in enumerate(sample_tickets, 1):
            try:
                # Select project in a round-robin fashion
                project_key = project_keys[i % len(project_keys)]
                
                print(f"📝 Creating ticket {i}/{len(sample_tickets)} in {project_key}: {ticket['summary'][:50]}...")
                
                # Temporarily override project_key
                original_project = self.jira.project_key
                self.jira.project_key = project_key
                
                result = self.jira.create_ticket(
                    summary=ticket["summary"],
                    description=ticket["description"],
                    issue_type=ticket["issue_type"]
                )
                
                # Restore original project_key
                self.jira.project_key = original_project
                
                created_tickets.append(result["key"])
                print(f"✅ Ticket created: {result['key']}")
                
                # Pause to avoid hitting API rate limits
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error creating ticket {i}: {e}")
                continue
        
        print(f"\n🎉 Done! {len(created_tickets)} tickets created:")
        for ticket_key in created_tickets:
            print(f"  - {ticket_key}")
            
        return created_tickets

def main():
    print("🎯 JIRA Seeder - Sample Ticket Generator")
    print("=" * 50)
    
    seeder = JiraSeeder()
    
    # Test connection
    if not seeder.jira.test_connection():
        print("❌ Error: Cannot connect to JIRA")
        print("Check credentials in your .env file")
        return
    
    print("✅ Connected to JIRA successfully")
    
    # Show project info if set
    if seeder.jira.project_key:
        try:
            project_info = seeder.jira.get_project_info()
            print(f"📋 Project: {project_info['name']} ({project_info['key']})")
        except Exception as e:
            print(f"⚠️ Could not retrieve project info: {e}")
    
    # Create sample tickets
    created_tickets = seeder.create_sample_tickets()
    
    if created_tickets:
        print(f"\n✨ Done! You can now run the classifier with:")
        print("python main.py")

if __name__ == "__main__":
    main()
