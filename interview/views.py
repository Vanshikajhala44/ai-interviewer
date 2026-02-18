# interview/views.py
import os, uuid
from django.shortcuts import render
from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.tts_service import text_to_audio
from .services.llm_service import get_ai_response,start_interview_ai,score_candidate_responses
from .services.stt_service import speech_to_text  
from io import BytesIO
from .services.storage_service import save_interview_entry
# from .services.score_service import score_answer

def home(request):
    return render(request, "interview/index.html")

@csrf_exempt
def start_interview(request):
    try:
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        ai_text = start_interview_ai(session_key)
        audio_url = text_to_audio(ai_text)

        request.session["conversation"] = [
            {"role": "ai", "content": ai_text}
        ]
        request.session["interview_active"] = True

        return JsonResponse({
            "ai_text": ai_text,
            "audio_url": audio_url,
            "interview_active": True
        })

    except Exception as e:
        print("FULL ERROR:", str(e))
        return JsonResponse({
            "error": str(e)
        }, status=500)


@csrf_exempt
def interview_view(request):
    try:
        if request.method != "POST":
            return JsonResponse({"error": "POST required"}, status=400)

        user_text = request.POST.get("audio_text", "").strip()
        session_key = request.session.session_key

        if not session_key or "interview_active" not in request.session:
            return JsonResponse({"error": "No active interview."}, status=400)

        # ---------------- SESSION TRACKING ----------------
        conversation = request.session.get("conversation", [])

        # Determine current question number
        candidate_count = sum(1 for c in conversation if c["role"] == "candidate")
        question_number = candidate_count + 1

        # ---------------- GENERATE NEXT AI QUESTION ----------------
        ai_text = get_ai_response(session_key, user_text)  # Only generates next question

        # ---------------- SAVE CANDIDATE RESPONSE ----------------
        save_interview_entry(
            session_key,
            "candidate",
            {
                "text": user_text,
                "question": ai_text  # store the question candidate answered
            }
        )

        # ---------------- SAVE AI QUESTION ----------------
        save_interview_entry(session_key, "ai", ai_text)

        # Save in session for frontend display
        conversation.append({"role": "candidate", "content": user_text, "question": ai_text})
        conversation.append({"role": "ai", "content": ai_text})
        request.session["conversation"] = conversation

        # ---------------- SCORE CANDIDATE RESPONSE ----------------
        # This will update the JSONL file with the numeric score
        score_result = score_candidate_responses(session_key)
        # Get the latest candidate score
        latest_score = score_result["details"][-1]["score"] if score_result["details"] else 0

        # ---------------- GENERATE AUDIO ----------------
        audio_url = text_to_audio(ai_text)

        return JsonResponse({
            "user_text": user_text,
            "ai_text": ai_text,
            "audio_url": audio_url,
            "question_number": question_number,
            "score": latest_score
        })

    except Exception as e:
        print("Error in interview_view:", str(e))
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def transcribe(request):
    if request.method != "POST" or "audio_file" not in request.FILES:
        return JsonResponse({"error": "POST with audio_file required"}, status=400)

    audio_file = request.FILES["audio_file"]

    try:
        # Read audio into memory
        audio_bytes = BytesIO()
        for chunk in audio_file.chunks():
            audio_bytes.write(chunk)
        audio_bytes.seek(0)  # Go to the start

        # Transcribe directly from memory (if your speech_to_text supports BytesIO)
        text = speech_to_text(audio_bytes)

        # Handle empty transcription
        if not text.strip():
            text = "[No speech detected]"

    except Exception as e:
        return JsonResponse({"text": "[no response]", "error": str(e)})

    return JsonResponse({"text": text})

# @csrf_exempt
# def transcribe(request):
#     if request.method != "POST" or "audio_file" not in request.FILES:
#         return JsonResponse({"error": "POST with audio_file required"}, status=400)

#     audio_file = request.FILES["audio_file"]

#     # Save file in MEDIA_ROOT instead of /tmp
#     os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
#     temp_filename = f"{uuid.uuid4()}.webm"
#     temp_path = os.path.join(settings.MEDIA_ROOT, temp_filename)

#     try:
#         with open(temp_path, "wb") as f:
#             for chunk in audio_file.chunks():
#                 f.write(chunk)

#         # Transcribe audio
#         text = speech_to_text(temp_path)

#     except Exception as e:
#         return JsonResponse({"text": "[no response]", "error": str(e)})

#     finally:
#         # Remove the temporary file
#         if os.path.exists(temp_path):
#             os.remove(temp_path)

#     return JsonResponse({"text": text})