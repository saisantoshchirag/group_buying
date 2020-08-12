from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib import messages
import hashlib
from profiles.models import UserProfile
from .forms import SignupForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import send_mail

def signup(request):
    print(' int ot the signup')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            print('user save')
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            data = {'user': user,
                    'domain': current_site.domain,
                    'uid':force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                    'token':account_activation_token.make_token(user),}
            message = render_to_string('Accounts/acc_active_email.html', data)
            to_email = form.cleaned_data.get('email')
            # to_email = 'saisantosh.c17@iiits.in'
            send_mail(mail_subject, message, 'santosh.265559@gmail.com', [to_email])

            return render(request,'Accounts/send.html')
    else:
        print('in to the else signup')
        form = SignupForm()
    return render(request, 'Accounts/signup.html', {'form': form})

def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('create')
    else:
        return HttpResponse('Activation link is invalid!')

def signin(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are Logged in.')
        return redirect('home')
    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'Accounts/login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        messages.success(request, 'You are Logged in.')

        try:
            UserProfile.objects.filter(user=request.user)
        except:
            return redirect('create')
        return redirect(request.GET.get('next','home'))
    else:
        messages.add_message(request, messages.WARNING, 'Invalid Login Credentials.')
        return redirect('login')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    messages.success(request, 'You are Successfully Logged Out')
    messages.success(request, 'Thanks for visiting')
    # messages.add_message(request, messages.INFO, 'Thanks for visiting.')
    return redirect('login')

def reset_display(request):
    return render(request,'Accounts/reset_form.html',{})


def reset_password(request):
    email = request.POST.get('email')
    user = User.objects.get(email=email)
    if user:
        current_site = get_current_site(request)
        mail_subject = 'Password reset link'
        data = {'user': user,
                'domain': current_site.domain,
                'uid':force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token':account_activation_token.make_token(user),}
        message = render_to_string('Accounts/reset_confirm_email.html', data)
        email = 'saisantosh.c17@iiits.in'
        send_mail(mail_subject, message, 'santosh.265559@gmail.com', [email])
        return render(request,'Accounts/password_reset_form.html')

    else:
        return redirect('registration:reset_display')

def verify_reset_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        login(request, user)
        # request.session['email'] = user['email']
        return render(request,'Accounts/save_password.html',{})
    else:
        return HttpResponse('Activation link is invalid!')


def save_password(request):
    email = request.user.email
    user = User.objects.get(email=email)
    # print(user)
    new_password  = request.POST.get('password')
    # print(new_password)
    password = hashlib.sha256(new_password.encode())
    password = password.hexdigest()
    user.set_password(new_password)
    user.save()
    return redirect('logout')