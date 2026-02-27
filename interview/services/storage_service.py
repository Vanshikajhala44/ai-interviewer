import os
import json
from datetime import datetime

INTERVIEW_DIR = "interview_data"
os.makedirs(INTERVIEW_DIR, exist_ok=True)

session_files = {}
session_scores = {}  # Single source of truth — remove import from llm_service

def create_session_file(session_key):
    # ✅ Guard: don't recreate if session already exists
    if session_key in session_files:
        return session_files[session_key]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"session_{timestamp}.jsonl"
    filepath = os.path.join(INTERVIEW_DIR, filename)
    session_files[session_key] = filepath
    session_scores[session_key] = 0
    return filepath

def evaluate_answer(answer_text):
    score = 0
    if len(answer_text) > 40:
        score += 2
    if len(answer_text) > 100:
        score += 3
    if "example" in answer_text.lower():
        score += 2
    if "django" in answer_text.lower():
        score += 1
    if "python" in answer_text.lower():
        score += 1
    return score

def save_entry(session_key, role, content, score=None, total_score=None):
    filepath = session_files.get(session_key)
    if not filepath:
        filepath = create_session_file(session_key)

    entry = {
        "session": session_key,
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    if score is not None:
        entry["score"] = score
    if total_score is not None:
        entry["total_score"] = total_score

    with open(filepath, "a") as f:
        f.write(json.dumps(entry) + "\n")

def save_score_to_db(session_key, interview_token, candidate_name, candidate_email):
    from interview.models import InterviewScore  # ✅ Lazy import avoids circular issues

    raw_score = session_scores.get(session_key, 0)
    print(raw_score)
    try:
        score_obj, created = InterviewScore.objects.get_or_create(
            interview_token=interview_token,
            defaults={
                "candidate_name": candidate_name,
                "candidate_email": candidate_email,
                "raw_score": raw_score,
            }
        )
        if not created:
            score_obj.raw_score = raw_score
            score_obj.save()
        print(f"✅ Score saved: {candidate_name} → {score_obj.percentage}%")
        return score_obj
    except Exception as e:
        print(f"❌ save_score_to_db error: {e}")
        return None