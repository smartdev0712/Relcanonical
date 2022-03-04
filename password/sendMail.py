from .utils import generate_reset_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes , force_str , DjangoUnicodeDecodeError
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from accounts.thread import EmailThread

def send_password_reset_mail(user,request):
    current_site = get_current_site(request)
    email_subject = f"Password reset on Relcanonical"

    # creates the body of the email dynamically
    email_body = render_to_string('password/resetMail.html', {
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.id)),
        "token":generate_reset_token.make_token(user)
    })
        # send the email to the user
    email = EmailMessage(subject=email_subject , body=email_body, from_email=settings.EMAIL_HOST,
                to=[user.email]
                )
    # # multithreadin so the app does not have to wait
    email_thread = EmailThread(email)
    email_thread.start()
    email_thread.join()