import os
import json

# ---------------- DIRECTORY SETUP ----------------
INTERVIEW_DIR = "interview_data"
os.makedirs(INTERVIEW_DIR, exist_ok=True)

# File to store all interview entries (candidate + AI)
INTERVIEW_FILE = os.path.join(INTERVIEW_DIR, "responses.jsonl")


# ---------------- SAVE INTERVIEW ENTRY ----------------
def save_interview_entry(session_key, role, content, score=None):
    """
    Save one entry (AI question or candidate response) to the log.
    Each line is a JSON object.
    
    Arguments:
    - session_key: unique identifier for the session
    - role: "candidate" or "ai"
    - content: text or dict (for candidate, can include 'text' + 'score')
    - score: optional numeric score (used for candidate answers)
    """
    entry = {
        "session": session_key,
        "role": role,
        "content": content
    }
    if score is not None:
        entry["score"] = score

    with open(INTERVIEW_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

