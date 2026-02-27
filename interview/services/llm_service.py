import os
from groq import Groq
from dotenv import load_dotenv
from interview.services.storage_service import save_entry, evaluate_answer, create_session_file, session_scores


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_sessions = {}

session_prompts = {}

DEFAULT_SYSTEM_PROMPT = """
You are a strict but friendly AI interviewer for a Django/Python intern.

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

After question 10, say: "Thank you, your interview is over."

INSTRUCTIONS:
- Only generate a single question at a time.
- Do not provide answers or explanations.
- Keep questions short (<40 words).
"""

def start_interview_ai(session_key: str, candidate_name: str = "Candidate", system_prompt: str = None) -> dict:
    """Start interview and return first question as dict"""
    create_session_file(session_key)
    
    # Use custom or default prompt
    prompt = system_prompt if system_prompt else DEFAULT_SYSTEM_PROMPT
    session_prompts[session_key] = prompt

    chat_sessions[session_key] = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Start the technical interview for {candidate_name}."}
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  
            messages=chat_sessions[session_key],
            temperature=0.1,
            max_tokens=120
        )

        ai_text = response.choices[0].message.content
        chat_sessions[session_key].append({"role": "assistant", "content": ai_text})
        save_entry(session_key, "ai", ai_text)

        # ✅ Return as dict to match views.py expectations
        return {
            "question": ai_text,
            "ai_text": ai_text
        }
    
    except Exception as e:
        print(f"❌ Groq API Error: {e}")
        return {
            "question": "Hello! Let's begin the interview. Tell me about yourself.",
            "ai_text": "Hello! Let's begin the interview. Tell me about yourself."
        }


def get_ai_response(session_key: str, user_text: str) -> dict:
    """Get next question after candidate answer"""
    prompt = session_prompts.get(session_key, DEFAULT_SYSTEM_PROMPT)
    
    if session_key not in chat_sessions:
        chat_sessions[session_key] = [{"role": "system", "content": prompt}]

    # Evaluate answer
    score = evaluate_answer(user_text)
    if session_key not in session_scores:
        session_scores[session_key] = 0
    session_scores[session_key] += score

    save_entry(
        session_key,
        "candidate",
        user_text,
        score=score,
        total_score=session_scores[session_key]
    )

    chat_sessions[session_key].append({"role": "user", "content": user_text})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ✅ Use valid Groq model
            messages=chat_sessions[session_key],
            temperature=0.3,
            max_tokens=120
        )

        ai_text = response.choices[0].message.content
        chat_sessions[session_key].append({"role": "assistant", "content": ai_text})
        save_entry(session_key, "ai", ai_text)

        return {
            "next_question": ai_text,
            "question": ai_text,
            "ai_text": ai_text
        }
    
    except Exception as e:
        print(f"❌ Groq API Error: {e}")
        return {
            "next_question": "Can you elaborate on that?",
            "question": "Can you elaborate on that?",
            "ai_text": "Can you elaborate on that?"
        }