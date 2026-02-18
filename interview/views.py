# interview/views.py
import os, uuid
from django.shortcuts import render
from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.tts_service import text_to_audio
from .services.llm_service import get_ai_response,start_interview_ai
from .services.stt_service import speech_to_text  
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


# ---------------- INTERVIEW STEP ----------------
@csrf_exempt
def interview_view(request):
    try:
        if request.method != "POST":
            return JsonResponse({"error": "POST required"}, status=400)

        user_text = request.POST.get("audio_text", "").strip()
        session_key = request.session.session_key

        if not session_key or "interview_active" not in request.session:
            return JsonResponse({"error": "No active interview."}, status=400)

        # Save candidate answer
        conversation = request.session.get("conversation", [])
        conversation.append({"role": "candidate", "content": user_text})

        # Generate AI response
        ai_text = get_ai_response(session_key, user_text)

        # Generate audio
        audio_url = text_to_audio(ai_text)

        # Save AI response
        conversation.append({"role": "ai", "content": ai_text})
        request.session["conversation"] = conversation

        return JsonResponse({
            "user_text": user_text,
            "ai_text": ai_text,
            "audio_url": audio_url
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