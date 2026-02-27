
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import CodingQuestion, CodeSubmission

from .services.groq import generate_coding_question
import json
import requests
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    return render(request, 'code_editor/index.html')



def generate_question(request):
    if request.method == "POST":
        data = json.loads(request.body)
        topic = data.get("topic", "Arrays")
        difficulty = data.get("difficulty", "medium")
        language = data.get("language", "python")

        # generate from groq
        question_data = generate_coding_question(topic, difficulty, language)

        # save to DB
        question = CodingQuestion.objects.create(
            topic=topic,
            difficulty=difficulty,
            language=language,
            title=question_data['title'],
            description=question_data['description'],
            example_input=question_data['example_input'],
            example_output=question_data['example_output'],
            constraints=question_data['constraints'],
            starter_code=question_data['starter_code']
        )

        return JsonResponse({
            "success": True,
            "question_id": question.id,
            "question": question_data
        })


def coding_round(request, question_id):
    question = CodingQuestion.objects.get(id=question_id)
    return render(request, 'code_editor/coding_round.html', {
        'question': question
    })


from django.conf import settings
import json
import requests
from django.http import JsonResponse

def run_code(request):
    if request.method == "POST":
        data = json.loads(request.body)
        code = data.get("code")
        language = data.get("language", "python")
        stdin = data.get("stdin", "")

        language_map = {
            'python': {'language': 'python3', 'versionIndex': '3'},
            'javascript': {'language': 'nodejs', 'versionIndex': '3'},
            'java': {'language': 'java', 'versionIndex': '3'},
            'cpp': {'language': 'cpp17', 'versionIndex': '0'},
        }

        lang_config = language_map.get(language, language_map['python'])

        # ✅ Get from settings
        client_id = settings.JDOODLE_CLIENT_ID
        client_secret = settings.JDOODLE_CLIENT_SECRET

        if not client_id or not client_secret:
            return JsonResponse({"error": "JDoodle credentials not configured"}, status=500)

        response = requests.post(
            "https://api.jdoodle.com/v1/execute",
            json={
                "clientId": client_id,
                "clientSecret": client_secret,
                "script": code,
                "stdin": stdin,
                "language": lang_config['language'],
                "versionIndex": lang_config['versionIndex'],
            }
        )

        result = response.json()

        return JsonResponse({
            "output": result.get("output", "No output"),
            "stderr": result.get("error", ""),
        })
        
def submit_code(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = CodingQuestion.objects.get(id=data.get("question_id"))

        submission = CodeSubmission.objects.create(
            question=question,
            language=data.get("language"),
            code=data.get("code"),
            output=data.get("output", ""),
            stderr=data.get("stderr", ""),
            status="Submitted"
        )

        return JsonResponse({
            "success": True,
            "redirect": f"/code/success/{submission.id}/"
        })

def success(request, submission_id):
    submission = CodeSubmission.objects.get(id=submission_id)
    return render(request, 'code_editor/success.html', {  # ← ye template exist karta hai?
        'submission': submission
    })
    
def start_coding_from_session(request):
    coding_question = request.session.get('coding_question', '')
    coding_topic = request.session.get('coding_topic', 'Arrays')
    coding_difficulty = request.session.get('coding_difficulty', 'medium')
    coding_language = request.session.get('coding_language', 'python')

    question = CodingQuestion.objects.create(
        topic=coding_topic,
        difficulty=coding_difficulty,
        language=coding_language,
        title="Coding Round",
        description=coding_question,
        example_input="",
        example_output="",
        constraints="",
        starter_code=""
    )
    return redirect(f'/code/coding-round/{question.id}/')