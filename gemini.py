from google import genai

# # === Paste your Gemini API key here ===
API_KEY = "AIzaSyBPLPmswxPSEMv5lgWppucskCVDlq78TCM"

# Initialize the Gemini client
client = genai.Client(api_key=API_KEY)

# Create a chat session with Gemini
chat_session = client.chats.create(
    model="gemini-2.5-flash"
)

# System prompt to make Gemini act like a professional interviewer
system_prompt = """
You are a professional software engineering interviewer.
- Ask behavioral and technical questions suitable for a B.Tech final-year student.
- Evaluate candidate answers, provide constructive feedback, and guide them.
- Keep the conversation professional and friendly.
- Start with the first question automatically.
"""

# Send the system prompt to start the interview
intro_response = chat_session.send_message(
    system_prompt + "\nInterviewer: Start the interview."
)
print("=== AI Interviewer ===")
print(intro_response.text)
print("-" * 50)

# --- Multi-turn interview loop ---
while True:
    candidate_input = input("Candidate answer: ")
    
    if candidate_input.lower() == "exit":
        print("Exiting interview. Goodbye!")
        break

    # Send candidate input to Gemini (do not include 'temperature')
    response = chat_session.send_message(candidate_input)

    # Print interviewer's response
    print("\nInterviewer response:\n", response.text)
    print("-" * 50)
