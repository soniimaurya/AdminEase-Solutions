def test_ai_ml_category():
    from app.processor import categorize_requirement

    result = categorize_requirement(
        "We need a machine learning chatbot"
    )

    assert result == "AI/ML Lead"