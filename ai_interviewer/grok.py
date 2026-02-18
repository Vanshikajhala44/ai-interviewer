import os
from groq import Groq

# Make sure your GROQ_API_KEY is set in your environment
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found! Set it in your environment.")

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Simple test: ask a question
prompt = "Hello Groq! Can you reply with a short greeting?"

try:
    response = client.chat(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
    )
    print("✅ Groq response:")
    print(response)
except Exception as e:
    print("❌ Error calling Groq API:", e)
