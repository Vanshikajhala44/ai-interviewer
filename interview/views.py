import os, uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.llm_service import start_interview_ai, get_ai_response
from .services.stt_service import speech_to_text
from .services.storage_service import save_entry
from io import BytesIO
from django.http import HttpResponse
import io
from gtts import gTTS

# interview/views.py
from django.views.decorators.http import require_GET
from urllib.parse import quote as urlquote
from .services.tts_service import text_to_audio_bytes


def tts_audio(request):
    text = request.GET.get("text","")
    if not text: return HttpResponse("No text", status=400)
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang="en")
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return HttpResponse(mp3_fp.read(), content_type="audio/mpeg")
def home(request):
    return render(request, "interview/index.html")

@csrf_exempt
def start_interview(request):
    try:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        ai_text = start_interview_ai(session_key)

        request.session["conversation"] = [{"role": "ai", "content": ai_text}]
        request.session["interview_active"] = True

        return JsonResponse({"ai_text": ai_text, "interview_active": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def transcribe(request):
    if request.method != "POST" or "audio_file" not in request.FILES:
        return JsonResponse(
            {"error": "POST with audio_file required"},
            status=400
        )

    audio_file = request.FILES["audio_file"]

    try:
        text = speech_to_text(audio_file)

        if not text.strip():
            text = "[No speech detected]"

        return JsonResponse({"text": text})

    except Exception as e:
        return JsonResponse({
            "text": "[no response]",
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

        # Process conversation
        ai_response = get_ai_response(session_key, user_text)

# If AI returns dictionary, extract text
        if isinstance(ai_response, dict):
          ai_text = ai_response.get("question") or ai_response.get("ai_text") or str(ai_response)
        else:
         ai_text = ai_response

        # Optionally save candidate response
        conversation = request.session.get("conversation", [])
        conversation.append({"role": "candidate", "content": user_text})
        conversation.append({"role": "ai", "content": ai_text})
        request.session["conversation"] = conversation

        # Return JSON
        return JsonResponse({
            "user_text": user_text,
            "ai_text": ai_text,
        })

    except Exception as e:
        # Catch ALL errors and return JSON
        print("Error in interview_view:", e)
        return JsonResponse({"error": str(e)}, status=500)

 