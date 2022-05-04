from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_verification_mail(code, email):
    subject = "Verification Mail"
    body = \
"""
Hello dear {0}, Welcome to our website.
Use the following code to login into our website
<b>Code: {1}</b>
Thanks for choosing us
""".format(email, code)
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject=subject, message="", html_message=body, from_email=from_email, recipient_list=[email])
    return 1