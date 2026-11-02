```python
from datetime import datetime, timezone


def categorize_requirement(requirement: str) -> str:
    """
    Automatically categorize leads based on their requirements.
    """

    text = requirement.strip().lower()

    categories = {
        "CRM Lead": [
            "crm",
            "customer relationship",
            "lead management",
            "customer management"
        ],

        "Website Lead": [
            "website",
            "web development",
            "web design",
            "landing page"
        ],

        "Automation Lead": [
            "automation",
            "workflow",
            "api",
            "integration",
            "process automation"
        ],

        "AI/ML Lead": [
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "chatbot",
            "generative ai",
            "nlp"
        ]
    }

    for category, keywords in categories.items():

        if any(keyword in text for keyword in keywords):
            return category

    return "General Lead"


def prepare_lead(lead_data: dict) -> dict:
    """
    Prepare lead data before database insertion.
    """

    requirement = lead_data["requirement"]

    return {
        **lead_data,
        "category": categorize_requirement(requirement),
        "status": "New",
        "received_at": datetime.now(
            timezone.utc
        ).isoformat()
    }
```
