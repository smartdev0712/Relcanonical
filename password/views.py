from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .sendMail import send_password_reset_mail
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes , force_str , DjangoUnicodeDecodeError
from .utils import generate_reset_token
from django.utils.http import urlsafe_base64_decode
from accounts.sendMail import send_update_mail

User = get_user_model()
def index(request):
    context = {
        "first_name":request.user.first_name
    }
    return render(request, 'password/index.html',context)

@login_required
def request(request):
    if request.method == 'POST':
        email = request.POST["account_email"]
        user = User.objects.get(email=email)
        send_password_reset_mail(user , request)
        return redirect("confirm")
    context = {
        "first_name":request.user.first_name,
        "email":request.user.email
    }

    return render(request, 'password/request.html',context)


@login_required
def confirm(request):
    context = {
        "first_name":request.user.first_name
    }
    return render(request, 'password/confirm.html',context)

@login_required
def change(request,uidb64,token):
    if request.method == 'POST':
        password = request.POST["new_password"]
        confirm_password = request.POST['confirm_password']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            query = User.objects.get(id=uid)
            if query and generate_reset_token.check_token(query,token):
                user = query
                if password == confirm_password:
                    user.set_password(password)
                    user.save()
                    send_update_mail(user)
                    return redirect('/password')
                else:
                    raise ValueError("Failed to reset password")
            else:
                raise ValueError("Password reset Failed")
        except Exception as e:
            print(e)
            query = None
            return redirect('/')
    return render(request, 'password/change.html')