from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()
    return {
        "JIRA_SERVER": os.getenv("JIRA_SERVER"),
        "JIRA_EMAIL": os.getenv("JIRA_EMAIL"),
        "JIRA_API_TOKEN": os.getenv("JIRA_API_TOKEN"),
    }
