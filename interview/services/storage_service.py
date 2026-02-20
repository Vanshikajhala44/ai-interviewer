import os
import json
from datetime import datetime

# ---------------- DIRECTORY SETUP ----------------
INTERVIEW_DIR = "interview_data"
os.makedirs(INTERVIEW_DIR, exist_ok=True)

session_files = {}     # stores file path per session
session_scores = {}    # stores total score per session

def create_session_file(session_key):
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

    return score  # Max ~9 per answer
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
