# interview/services/llm_service.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_sessions = {}
SYSTEM_PROMPT = """
You are a strict but friendly AI interviewer for Vanshika, a Django/Python intern.

RULES:
- Only ask the next question, never answer for the candidate.
- There are exactly 10 questions in this order:
  1. What is Python and why is it popular?
  2. Explain Python data types.
  3. What is Django and why use it?
  4. Explain Django models and migrations.
  5. What is a Django view? Difference between function-based and class-based views?
  6. How do you handle forms in Django?
  7. What is Django ORM? Give an example.
  8. Explain URL routing in Django.
  9. How do you use templates in Django?
  10. What is a REST API and how would you implement it in Django?

INSTRUCTIONS:
- Only generate a single question at a time.
- Do not provide answers or explanations.
- Always ask the next unanswered question based on the session's candidate responses.
- If the candidate hasn’t answered yet, repeat the last question.
- Keep questions short (<40 words).
"""



# SYSTEM_PROMPT = """
# You are a strict but friendly software engineering interviewer.

# Rules:
# - Only ask questions.
# - Never answer for the candidate.
# - Always ask one follow-up question based on the candidate's previous answer.
# - Keep responses under 40 words.
# """

def start_interview_ai(session_key):
    chat_sessions[session_key] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Start the technical interview."}
    ]

    response = client.chat.completions.create(
        model="groq/compound",
        messages=chat_sessions[session_key],
        temperature=0.1,
        max_tokens=120
    )

    ai_text = response.choices[0].message.content

    chat_sessions[session_key].append(
        {"role": "assistant", "content": ai_text}
    )

    return ai_text


def get_ai_response(session_key, user_text):
    if session_key not in chat_sessions:
        chat_sessions[session_key] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    # Add candidate answer (MUST be last before API call)
    chat_sessions[session_key].append(
        {"role": "user", "content": user_text}
    )

    response = client.chat.completions.create(
        model="groq/compound",
        messages=chat_sessions[session_key],
        temperature=0.3,
        max_tokens=120
    )

    ai_text = response.choices[0].message.content

    chat_sessions[session_key].append(
        {"role": "assistant", "content": ai_text}
    )

    return ai_text

# interview/services/llm_service.py
import os
import json
from groq import Groq

# Load your Groq API key via dotenv somewhere at the top of the file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

INTERVIEW_FILE = "interview_data/responses.jsonl"

def score_candidate_responses(session_key):
    """
    Reads candidate responses from the JSONL file, sends each to Groq for scoring,
    and updates the file with a numeric score out of 10.
    Returns total score and per-question details.
    """
    if not os.path.exists(INTERVIEW_FILE):
        return {"session": session_key, "total_score": 0, "details": []}

    entries = []
    with open(INTERVIEW_FILE, "r") as f:
        for line in f:
            entry = json.loads(line)
            if entry.get("session") == session_key:
                entries.append(entry)

    scored_entries = []
    total_score = 0
    score = 5

#     for entry in entries:
#         if entry["role"] == "candidate" and "score" not in entry:
#             candidate_text = entry["content"]
#             question = entry.get("question", "Unknown question")

#             prompt = f"""
# You are an interviewer evaluating a candidate.
# Question: "{question}"
# Candidate answer: "{candidate_text}"
# Score the answer from 0 to 10 based on accuracy and completeness.
# Only return the numeric score.
# """
#             try:
#                 response = client.chat.completions.create(
#                     model="groq/compound",
#                     messages=[{"role": "user", "content": prompt}],
#                     temperature=0
#                 )
#                 score_text = response.choices[0].message.content.strip()
#                 score = int(score_text)
#             except Exception as e:
#                 print("Scoring error:", e)
#                 score = 0

#             # Save score in memory
#             entry["score"] = score
#             scored_entries.append({
#                 "question": question,
#                 "answer": candidate_text,
#                 "score": score
#             })
#             total_score += score
    for entry in entries:
     if entry["role"] == "candidate":
        candidate_content = entry["content"]
        candidate_text = candidate_content["text"]
        question = candidate_content.get("question", "Unknown question")

        # Only score if missing or zero
        if entry.get("score", 0) == 0:
            prompt = f"""
You are an interviewer evaluating a candidate.
Question: "{question}"
Candidate answer: "{candidate_text}"
Score  answer  to 10 
Only return the numeric score.
"""

            try:
                response = client.chat.completions.create(
                    model="groq/compound",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0
                )

                score_text = response.choices[0].message.content.strip()

                # Safe parsing
                import re
                match = re.search(r"\d+", score_text)
                score = int(match.group()) if match else 0

                entry["score"] = score

            except Exception as e:
                print("Scoring error:", e)
                entry["score"] = 15

    # Rewrite the file with updated scores
    with open(INTERVIEW_FILE, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    return {"session": session_key, "total_score": score, "details": scored_entries}
