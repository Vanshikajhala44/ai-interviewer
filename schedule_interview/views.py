from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import SecretInterview
from .forms import InterviewForm
from django.urls import reverse
from .email_service import send_interview_invitation 
from functools import wraps

STATIC_INTERVIEWERS = [
    {
        "name": "vanshika",
        "email": "vanshikajhala009@gmail.com",
        "password": "vansh123",
        "role": "interviewer"
    }
]

def interviewer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("interviewer_logged_in"):
            return redirect("schedule_interview:interviewer_login")
        return view_func(request, *args, **kwargs)
    return wrapper

@interviewer_required
def schedule_interview(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = SecretInterview.objects.create(
                candidate_name=form.cleaned_data['candidate_name'],
                candidate_email=form.cleaned_data['candidate_email'],
                interviewer_name=form.cleaned_data['interviewer_name'],
                system_prompt=form.cleaned_data['system_prompt'],
                interview_datetime=form.cleaned_data['interview_datetime'],
                expires_at=form.cleaned_data.get('expires_at'),
                coding_question=form.cleaned_data.get('coding_question', ''),
                coding_topic=form.cleaned_data.get('coding_topic', 'Arrays'),
                coding_difficulty=form.cleaned_data.get('coding_difficulty', 'medium'),
                coding_language=form.cleaned_data.get('coding_language', 'python'),
            )
            interview_link = request.build_absolute_uri(
                reverse('schedule_interview:verify_passcode', kwargs={'token': interview.token})
            )
            send_interview_invitation(
                candidate_name=interview.candidate_name,
                candidate_email=interview.candidate_email,
                interview_link=interview_link,
                interview_datetime=interview.interview_datetime,
                passcode=interview.passcode,
            )
            return redirect('schedule_interview:schedule_success', token=interview.token)
    else:
        form = InterviewForm()
    return render(request, 'schedule_interview/form.html', {'form': form})


def schedule_success(request, token):
    interview = SecretInterview.objects.get(token=token)
    interview_link = request.build_absolute_uri(
        reverse('schedule_interview:verify_passcode', kwargs={'token': interview.token})
    )
    return render(request, 'schedule_interview/success.html', {
        'interview': interview,
        'interview_link': interview_link,
        'passcode': interview.passcode,
    })


def verify_passcode(request, token):
    secret = get_object_or_404(SecretInterview, token=token)

    if secret.expires_at and timezone.now() > secret.expires_at:
        return render(request, 'schedule_interview/expired.html')

    if secret.used:
        return render(request, 'schedule_interview/expired.html')

    error = None
    if request.method == 'POST':
        entered = request.POST.get('passcode', '').strip()
        if entered == secret.passcode:
            secret.used = True
            secret.save()

            request.session['candidate_name'] = secret.candidate_name
            request.session['candidate_email'] = secret.candidate_email
            request.session['interviewer_name'] = secret.interviewer_name
            request.session['system_prompt'] = secret.system_prompt
            request.session['interview_datetime'] = secret.interview_datetime.isoformat()
            request.session['coding_question'] = secret.coding_question
            request.session['coding_topic'] = secret.coding_topic
            request.session['coding_difficulty'] = secret.coding_difficulty
            request.session['coding_language'] = secret.coding_language
            request.session['interview_token'] = str(secret.token)

            return redirect(reverse('interview:home'))
        else:
            error = '❌ Invalid passcode. Please check your email and try again.'

    return render(request, 'schedule_interview/verify_passcode.html', {
        'error': error,
        'candidate_name': secret.candidate_name,
    })


def start_interview_from_link(request, token):
    return redirect('schedule_interview:verify_passcode', token=token)


def interviewer_login(request):
    if request.session.get("interviewer_logged_in"):
        return redirect("schedule_interview:schedule_interview")

    error = None
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        matched_user = None
        for user in STATIC_INTERVIEWERS:
            if user["email"] == email:
                matched_user = user
                break

        if not matched_user:
            error = "❌ Email not found. Please check your email."
        elif matched_user["password"] != password:
            error = "❌ Wrong password. Please try again."
        elif matched_user["role"] != "interviewer":
            error = "🚫 Access denied. You don't have interviewer privileges."
        else:
            request.session["interviewer_logged_in"] = True
            request.session["interviewer_name"] = matched_user["name"]
            return redirect("schedule_interview:schedule_interview")

    return render(request, "schedule_interview/login.html", {"error": error})


def interviewer_logout(request):
    request.session.flush()
    return redirect("schedule_interview:interviewer_login")