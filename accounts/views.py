from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import Request
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes , force_str , DjangoUnicodeDecodeError
from .utils import generateToken
from django.conf import settings
from django.http import Http404
from django.contrib.auth import get_user_model , authenticate , login , logout
from .sendMail import send_activation_mail , send_update_mail
from django.contrib.auth.decorators import login_required
from .models import UserAccount
User = get_user_model()

def request(request):
    if request.method == "POST":
        # get post data
        post_data = request.POST
        first_name = post_data['first_name']
        last_name = post_data['last_name']
        email=post_data['account_email']

        # check if a user has already made a request
        account_request = Request.objects.filter(email=email)
        if len(account_request) > 0:
            if account_request[0].is_email_verified:
                return redirect('onboard',uid=account_request[0].id)
            else:
                send_activation_mail(account_request[0], request)
                return redirect('confirm')

        # create a new request
        new_request = Request.objects.create(first_name=first_name, last_name=last_name,email=email)
        # send user activation mail
        send_activation_mail(new_request , request)
        # redirect user to confirm page
        return redirect(f'/account/request/confirm?first_name={first_name}')

    return render(request, 'account/request.html')

def confirm(request):
    context = {
        "first_name":request.GET.get('first_name')
    }
    return render(request, 'account/confirm.html',context)

# the is asked to visit this view in his email to verify his email
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        query = Request.objects.get(id=uid)
        if query and generateToken.check_token(query,token):
            query.is_email_verified=True
            #verify the user and then redirect to onboard page
            query.save()
            token=generateToken(query)
            return redirect('onboard',uidb64=uidb64,token=token)
        else :
            return render("/accounts/requestFailed.html")
    except Exception as e:
        print(e)
        query = None
        return redirect('/accounts/requestFailed.html')


def onboard(request,uidb64,token):
    data = request.GET
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        if uid and generateToken.check_token(token):
            account_request = Request.objects.get(id=uid)
    except Request.DoesNotExist:
        raise Http404("No request found")

    if request.method == 'POST':
        password = request.POST["create_password"]
        confirm_password = request.POST['confirm_password']

        # check if a user with this email already exits
        if len(User.objects.filter(email=account_request.email)) > 0:
            raise ValueError("A user with this email already exists")

        if password == confirm_password:
            user = User(first_name=account_request.first_name,
                        last_name=account_request.last_name,
                        email=account_request.email,
                        is_email_verified=account_request.is_email_verified)
            user.set_password(password)
            user.save()
            # each a user creates an account he his linked to user account as a foreign key , which stores his account plan
            UserAccount.objects.create(user=user)
            return redirect('/account/access')
        else:
            raise ValueError("The two password fields don't match")
    return render(request, 'account/onboard.html')

def access(request):
    if request.method == 'POST':
        email = request.POST["account_email"]
        password = request.POST['account_password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request , user)
            return redirect('/account')
    return render(request, 'account/access.html')

# you need to be logged in to update your account
def update(request):
    user = request.user
    print(request.user)
    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST['last_name']
        password = request.POST['change_password']
        confirm_password = request.POST['confirm_password']
        # update user
        if password == confirm_password:
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()
            send_update_mail(user)
        else :
            raise ValueError("The two passwords do no match")
        # send mail to user
        send_update_mail(user)
        # redirect user to account
        return redirect('/account')
    return render(request, 'account/update.html')

@login_required
def index(request):
    user = request.user
    context = {
        "first_name":user.first_name
    }
    return render(request, 'account/index.html',context)

def exit(request):
    logout(request)
    return redirect('/account/access/')

@login_required
def script(request):
    return render(request, 'account/script.html')
