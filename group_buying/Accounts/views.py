from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group

# Create your views here.
def login(request):
	if request.user.is_authenticated:
		messages.add_message(request, messages.INFO, 'You are already Logged in.')
		return HttpResponse('you are logged in')
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
		messages.add_message(request, messages.INFO, 'Your are now Logged in.')
		return HttpResponse('you are logged in')
	else:
		messages.add_message(request, messages.WARNING, 'Invalid Login Credentials.')
		return HttpResponseRedirect('/loginmodule/auth')

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
	messages.add_message(request, messages.INFO, 'You are Successfully Logged Out')
	messages.add_message(request, messages.INFO, 'Thanks for visiting.')
	return HttpResponseRedirect('/login')



def register(request):
    print("\n\n",'Enter register')
    
    if request.method == 'POST':
        choice = request.POST['choice']
        print(choice)
        print('entered if of post and files')
        u_form = CustomUserCreationForm(data=request.POST)
        print(u_form['choice'])
        if u_form.is_valid():
            print('u form validation done ')
            
                
            user = u_form.save()
                # user.is_active = False
            user.set_password(user.password)
            print('helloooo','password set')
            # group = Group.objects.get(name=choice)
            # user.groups.add(group)

            user.save()

                
            return redirect('/login')
    else:
        u_form = CustomUserCreationForm()
        # p_form = Createprofileform()

    return render(request, 'Accounts/register.html', {'u_form': u_form})
