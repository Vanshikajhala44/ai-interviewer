from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_interview_invitation(candidate_name, candidate_email, interview_link, interview_datetime, passcode):
    try:
        subject = f'Your Interview is Scheduled - {interview_datetime.strftime("%B %d, %Y at %I:%M %p")}'

        html_content = render_to_string('schedule_interview/email_template.html', {
            'candidate_name': candidate_name,
            'interview_link': interview_link,
            'interview_datetime': interview_datetime.strftime("%B %d, %Y at %I:%M %p"),
            'passcode': passcode,
        })

        text_content = f"""
Dear {candidate_name},

Your interview has been scheduled for {interview_datetime.strftime("%B %d, %Y at %I:%M %p")}.

YOUR PASSCODE: {passcode}
Keep this confidential!

Interview Link: {interview_link}

Steps:
1. Click the link
2. Enter passcode: {passcode}
3. Allow camera & microphone
4. Use Google Chrome

Good luck!
Interview Team
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[candidate_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        logger.info(f"✅ Email sent to {candidate_email}")
        return True

    except Exception as e:
        logger.error(f"❌ Email failed: {str(e)}")
        return False