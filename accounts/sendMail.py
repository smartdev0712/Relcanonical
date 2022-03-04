from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
import smtplib , ssl
from django.conf import settings
from .thread import EmailThread
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes , force_str , DjangoUnicodeDecodeError
from .utils import generateToken

    # context = ssl.create_default_context()
    # with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
    #     server.ehlo()  # Can be omitted
    #     server.starttls(context=context)
    #     server.ehlo()  # Can be omitted
    #     server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    #     server.sendmail(settings.EMAIL_HOST_USER, new_request.email, email_body)


# sends account activation mails
def send_activation_mail(new_request , request):
    current_site = get_current_site(request)
    email_subject = f"Account email verification on Relcanonical"
    # # creates the body of the email dynamically with a template
    email_body = render_to_string('account/activateMail.html', {
        'new_request':new_request,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(new_request.id)),
        "token":generateToken.make_token(new_request)
    })
    # # send the email to the user
    email = EmailMessage(subject=email_subject , body=email_body, from_email=settings.EMAIL_HOST,
                to=[new_request.email]
                )
    # # multithreadin so the app does not have to wait
    email_thread = EmailThread(email)
    email_thread.start()
    email_thread.join()

# sends account update mails
def send_update_mail(user):
    email_subject = 'Account Update on Recanonical'
    email_body = render_to_string('account/updateMail.html',{
        "first_name":user.first_name
    })
    email = EmailMessage(subject=email_subject , body=email_body, from_email=settings.EMAIL_HOST,
                to=[user.email]
                )
    email_thread = EmailThread(email)
    email_thread.start()
    email_thread.join()

def send_password_reset_mail(user , request):
    current_site = get_current_site(request)
    email_subject = f"Password reset on Relcanonical"
    # creates the body of the email dynamically using a mail template
    email_body = render_to_string('account/passwordResetMail.html', {
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.id)),
        "token":generateToken.make_token(user)
    })
    # send the email to the user
    email = EmailMessage(subject=email_subject , body=email_body, from_email=settings.EMAIL_HOST,
                to=[user.email]
                )
    # multithreadin so the app does not have to wait
    email_thread = EmailThread(email)
    email_thread.start()
    email_thread.join()
