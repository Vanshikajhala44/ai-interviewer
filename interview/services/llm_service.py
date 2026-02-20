import os
from groq import Groq
from dotenv import load_dotenv
from interview.services.storage_service import save_entry, evaluate_answer,create_session_file

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_sessions = {}
session_scores = {}

SYSTEM_PROMPT = """
You are a strict but friendly AI interviewer for Vanshika, a Django/Python intern.

RULES:
dont answer the question just ask these question
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
  after this just say thankyou your interview is over

INSTRUCTIONS:
- Only generate a single question at a time.
- Do not provide answers or explanations.
- Always ask the next unanswered question based on the session's candidate responses.
- If the candidate hasn’t answered yet, repeat the last question.
- Keep questions short (<40 words).
"""

def start_interview_ai(session_key: str) -> str:
    create_session_file(session_key)

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
    chat_sessions[session_key].append({"role": "assistant", "content": ai_text})

    save_entry(session_key, "ai", ai_text)

    return ai_text


def get_ai_response(session_key: str, user_text: str) -> dict:
    if session_key not in chat_sessions:
        chat_sessions[session_key] = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Calculate score
    score = evaluate_answer(user_text)

    # Make sure session score exists
    if session_key not in session_scores:
        session_scores[session_key] = 0

    # Update total session score
    session_scores[session_key] += score

    # Save candidate response with score
    save_entry(
    session_key,
    "candidate",
    user_text,
    score=score,
    total_score=session_scores[session_key])

    chat_sessions[session_key].append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model="groq/compound",
        messages=chat_sessions[session_key],
        temperature=0.3,
        max_tokens=120
    )

    ai_text = response.choices[0].message.content
    chat_sessions[session_key].append({"role": "assistant", "content": ai_text})

    save_entry(session_key, "ai", ai_text)

    return {
        "next_question": ai_text
    }
