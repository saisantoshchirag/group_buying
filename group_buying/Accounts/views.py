from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib import messages
from .forms import CustomUserCreationForm,SignupForm
from django.contrib.auth.models import Group
# import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
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
            print(message,to_email)
            print(to_email)
            to_email = 'saisantosh.c17@iiits.in'
            send_mail(mail_subject, message, 'santosh.265559@gmail.com', [to_email])
            
            return render(request,'Accounts/send.html')
    else:
        print('in to the else signup')
        form = SignupForm()
    return render(request, 'Accounts/signup.html', {'form': form})

def activate(request, uidb64, token):
    # try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def signin(request):
	if request.user.is_authenticated:
		messages.add_message(request, messages.INFO, 'You are already Logged in.')
		return redirect('home')
	else:
		c = {}
		c.update(csrf(request))
		return render(request, 'Accounts/login.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	email = request.POST.get('email','')
	user = auth.authenticate(username=username, password=password)
	
	if user is not None:
		auth.login(request, user)
		messages.add_message(request, messages.INFO, 'Your are now Logged in.')
		return redirect('home')
	else:
		messages.add_message(request, messages.WARNING, 'Invalid Login Credentials.')
		return redirect('Accounts:login')

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
	messages.add_message(request, messages.INFO, 'You are Successfully Logged Out')
	messages.add_message(request, messages.INFO, 'Thanks for visiting.')
	return redirect('Accounts:login')

