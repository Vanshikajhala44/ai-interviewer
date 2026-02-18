# interview/services/scoring_service.py

SCORING_KEYWORDS = {
    1: ["python", "easy", "readable", "popular", "interpreted"],
    2: ["int", "float", "string", "list", "tuple", "dict", "set", "bool"],
    3: ["django", "framework", "web", "rapid", "development", "mvc"],
    4: ["model", "migration", "database", "fields", "schema"],
    5: ["view", "function-based", "class-based", "request", "response"],
    6: ["form", "validation", "POST", "cleaned_data", "ModelForm"],
    7: ["ORM", "queryset", "filter", "create", "update"],
    8: ["urls", "routing", "path", "re_path", "include"],
    9: ["template", "render", "context", "html", "django template"],
    10:["REST", "API", "GET", "POST", "serializer", "DRF"]
}

def score_answer(question_number, candidate_text):
    """
    Returns a score from 0 to 10 based on keyword presence.
    """
    keywords = SCORING_KEYWORDS.get(question_number, [])
    if not keywords or not candidate_text.strip():
        return 0

    text_lower = candidate_text.lower()
    matches = sum(1 for kw in keywords if kw in text_lower)
    
    # Scale to 10 points
    score = (matches / len(keywords)) * 10
    return round(score)
