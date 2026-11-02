from app.processor import categorize_requirement

def test_crm_category():
    assert categorize_requirement("CRM automation") == "CRM Lead"

def test_website_category():
    assert categorize_requirement("Website development") == "Website Lead"

def test_general_category():
    assert categorize_requirement("Need business consulting") == "General Lead"
def test_ai_ml_category():
    from app.processor import categorize_requirement

    result = categorize_requirement(
        "We need a machine learning chatbot"
    )

    assert result == "AI/ML Lead"