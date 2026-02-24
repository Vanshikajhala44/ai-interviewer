from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import SecretInterview
from .forms import InterviewForm
from django.urls import reverse

# def home(request):
#     return render(request, "schedule_interview/form.html")

def schedule_interview(request):
    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            secret = SecretInterview.objects.create(
                candidate_name=form.cleaned_data['candidate_name'],
                candidate_email=form.cleaned_data['candidate_email'],
                interviewer_name=form.cleaned_data['interviewer_name'],
                system_prompt=form.cleaned_data['system_prompt'],
                interview_datetime=form.cleaned_data['interview_datetime'],
                expires_at=form.cleaned_data.get('expires_at')
            )
            # Build absolute secret link
            link = request.build_absolute_uri(f"/schedule_interview/secret/{secret.token}/")
            return render(request, "schedule_interview/success.html", {"link": link})
    else:
        form = InterviewForm()
    return render(request, "schedule_interview/form.html", {"form": form})

def start_interview_from_link(request, token):
    secret = get_object_or_404(SecretInterview, token=token)

    # Check if link is already used or expired
    if secret.used or (secret.expires_at and timezone.now() > secret.expires_at):
        return render(request, "schedule_interview/expired.html")

    # Mark as used
    secret.used = True
    secret.save()

    # Save candidate info in session
    request.session['candidate_name'] = secret.candidate_name
    request.session['candidate_email'] = secret.candidate_email
    request.session['interviewer_name'] = secret.interviewer_name
    request.session['system_prompt'] = secret.system_prompt
    request.session['interview_datetime'] = secret.interview_datetime.isoformat()

    # Redirect to interview app home
    return redirect(reverse("interview:home"))