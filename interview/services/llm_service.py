# interview/services/llm_service.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_sessions = {}
# SYSTEM_PROMPT = """
# You are a friendly AI interviewer for Vanshika, a Python and Django intern. 
# Start by introducing yourself briefly: 'Hello Vanshika! I am your AI interviewer. Let's start your Python and Django interview.'
# Ask only **one question at a time**. 
# Do not give answers, hints, or explanations. Wait for the candidate's response before asking the next question.

# Questions (ask in order):
# 1. What is Python?
# 2. What are Python data types?
# 3. Explain Python functions.
# 4. What is Django?
# 5. Explain Django MVT architecture.
# 6. How do you create a model in Django?
# 7. How do you get data using QuerySets?
# 8. What is a Django view?
# 9. How do you handle forms in Django?
# 10. How do you run a Django project locally?
# """



SYSTEM_PROMPT = """
You are a strict but friendly software engineering interviewer.

Rules:
- Only ask questions.
- Never answer for the candidate.
- Always ask one follow-up question based on the candidate's previous answer.
- Keep responses under 40 words.
"""

def start_interview_ai(session_key):
    chat_sessions[session_key] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Start the technical interview."}
    ]

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
