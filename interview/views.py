import uuid, io, json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS

from .services.llm_service import start_interview_ai, get_ai_response
from .services.storage_service import save_entry

# =================== Home Page ===================
def home(request):
    """Render the interview page"""
    if not request.session.get('candidate_name'):
        return render(request, 'interview/unauthorized.html')
    
    return render(request, 'interview/index.html')  


# =================== Text-to-Speech ===================
def tts_audio(request):
    text = request.GET.get("text", "")
    if not text:
        return HttpResponse("No text provided", status=400)
    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang="en")
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return HttpResponse(mp3_fp.read(), content_type="audio/mpeg")
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        return HttpResponse(str(e), status=500)


# =================== Start Interview ===================
@csrf_exempt
def start_interview(request):
    """Start interview, initialize session & first AI question"""
    if request.method != 'POST':
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        # Get candidate info from session
        candidate_name = request.session.get('candidate_name', 'Candidate')
        system_prompt = request.session.get('system_prompt')  # ✅ FIXED - None by default

        # Initialize session
        session_key = str(uuid.uuid4())
        request.session['session_key'] = session_key
        request.session['conversation'] = []
        request.session['interview_active'] = True
        request.session.modified = True

        print(f"✅ Starting interview - Session: {session_key}")

        # Get first AI question
        ai_response = start_interview_ai(
            session_key=session_key,
            candidate_name=candidate_name,
            system_prompt=system_prompt
        )
        ai_text = ai_response.get("question") or ai_response.get("ai_text") or "Hello, let's start the interview."

        # Store AI message
        request.session['conversation'].append({"role": "ai", "content": ai_text})
        request.session.modified = True

        print(f"✅ First question: {ai_text[:60]}...")

        return JsonResponse({"ai_text": ai_text})

    except Exception as e:
        print(f"❌ Start Interview Error: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


# =================== Interview Answer Handling ===================
@csrf_exempt
def interview_view(request):
    """Receive candidate answer → return next AI question"""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        data = json.loads(request.body)
        user_text = data.get("audio_text", "").strip()
        if not user_text:
            return JsonResponse({"error": "Empty input"}, status=400)

        session_key = request.session.get("session_key")
        if not session_key or not request.session.get("interview_active"):
            return JsonResponse({"error": "No active interview"}, status=400)

        conversation = request.session.get("conversation", [])
        ai_questions_count = len([msg for msg in conversation if msg["role"] == "ai"])

        print(f"📝 Processing answer #{ai_questions_count}")

        if ai_questions_count >= 10:  # Max questions
            ai_text = "Thank you, your interview is over."
            interview_complete = True
            request.session["interview_active"] = False
            print("✅ Interview completed (10 questions reached)")
        else:
            ai_response = get_ai_response(session_key, user_text)
            ai_text = ai_response.get("next_question") or ai_response.get("question") or ai_response.get("ai_text") or "Next question..."
            interview_complete = False
            print(f"✅ Next question: {ai_text[:60]}...")

        # Append candidate answer + AI response
        conversation.append({"role": "candidate", "content": user_text})
        conversation.append({"role": "ai", "content": ai_text})
        request.session["conversation"] = conversation
        request.session.modified = True

        return JsonResponse({
            "user_text": user_text,
            "ai_text": ai_text,
            "interview_complete": interview_complete
        })

    except Exception as e:
        print(f"❌ Interview View Error: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


# =================== End Interview ===================

@csrf_exempt
def end_interview(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        request.session['interview_active'] = False
        conversation    = request.session.get('conversation', [])
        session_key     = request.session.get('session_key')
        interview_token = request.session.get('interview_token')   # ← new
        candidate_name  = request.session.get('candidate_name')
        candidate_email = request.session.get('candidate_email')

        # 1. Audit log (.jsonl) - same as before
        

        # 2. ✅ THE BRIDGE - DB mein save
        if session_key and interview_token:
            from interview.services.storage_service import save_score_to_db
            score_obj = save_score_to_db(
                session_key     = session_key,
                interview_token = interview_token,
                candidate_name  = candidate_name,
                candidate_email = candidate_email
            )
            if score_obj:
                return JsonResponse({
                    "status"    : "ok",
                    "score"     : score_obj.raw_score,
                    "percentage": score_obj.percentage,
                })

        return JsonResponse({"status": "ok"})

    except Exception as e:
        print(f"❌ End Interview Error: {e}")
        return JsonResponse({"error": str(e)}, status=500)