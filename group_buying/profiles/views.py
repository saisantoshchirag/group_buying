from django.shortcuts import render,redirect
from .models import UserProfile,ChangePassword
from .forms import UpdateForm
import re
from django.http import HttpResponse
from twilio.rest import Client
from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

@login_required(login_url='/loginmodule/login/')
def update(request):
    current_user = UserProfile.objects.filter(user=request.user).values()
    cur_gender = current_user[0].get('gender')
    cur_state = current_user[0].get('state')
    cur_pincode = current_user[0].get('pincode')
    cur_city = current_user[0].get('city')
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                myfile = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                UserProfile.objects.filter(user=request.user).update(image=request.FILES['image'])
            except:
                pass
            try:
                UserProfile.objects.filter(user=request.user).update(gender=request.POST['gender'])
            except:
                UserProfile.objects.filter(user=request.user).update(gender=cur_gender)
            try:
                UserProfile.objects.filter(user=request.user).update(city=request.POST['city'])
            except:
                UserProfile.objects.filter(user=request.user).update(city=cur_city)
            try:
                UserProfile.objects.filter(user=request.user).update(state=request.POST['state'])
            except:
                UserProfile.objects.filter(user=request.user).update(state=cur_state)
            try:
                UserProfile.objects.filter(user=request.user).update(pincode=request.POST['pincode'])
            except:
                UserProfile.objects.filter(user=request.user).update(pincode=cur_pincode)
            return redirect('view')
    else:
        form = UpdateForm()
    return render(request,'profiles/update.html',{'form':form})

@login_required(login_url='/loginmodule/login/')
def profile(request):
    user = UserProfile.objects.filter(user=request.user).values()
    if not user:
        return redirect('create')
    return render(request,'profiles/profile.html',{'user':request.user})

@login_required(login_url='/loginmodule/login/')
def create(request):
    if request.method == 'POST':
        pincode = request.POST.get('pincode')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        gender = request.POST.get('gender')
        # image = request.FILES['image']
        UserProfile.objects.create(state=state,city=city,gender=gender,pincode=pincode,phone_number=phone_number,user=request.user)
        return redirect(request.GET.get('next','view'))
    return render(request,'profiles/create.html')

def phone_number(request):
    user = request.user
    return render(request,'profiles/change_phone_number.html')

def change_phone(request):
    if request.method=='POST':
        user = UserProfile.objects.filter(user=request.user).values()
        if user:
            phone_cur = user[0]['phone_number']
        phone = request.POST['phone_number']
        if isValid(phone):
            phone = phone[-10:]
        if str(phone_cur) == phone:
            return HttpResponse('<html><script>alert("You have entered your current phone number!Please enter another number");window.location="/profile/phone";</script></html>')
        if not isValid(phone):
            return HttpResponse('<html><script>alert("You have entered invalid phone number .Please check");window.location="/profile/phone";</script></html>')
        code = get_random_string(length=6,allowed_chars='0123456789')
        otps = ChangePassword.objects.filter(user=request.user)
        if otps:
            ChangePassword.objects.filter(user=request.user).delete()
        ChangePassword.objects.create(user=request.user,code=code,phone_number=phone)
        account_sid = 'ACc3334be22f266fb10c6ce4e77a660264'
        auth_token = '9077db471beb2d47a3ea60e0382b8aef'
        client = Client(account_sid, auth_token)
        body = 'Please verify your phone number.OTP: '+str(code) + '. Do not share with anyone!!!'
        message = client.messages.create(
            body=body,
            from_='+12058436831',
            to='+91' + str(phone)
        )
    return render(request,'profiles/otp.html')

def validate_otp(request):
    obj = ChangePassword.objects.filter(user=request.user).values()
    if request.POST['otp'] == str(obj[0]['code']):
        UserProfile.objects.filter(user=request.user).update(phone_number=obj[0]['phone_number'])
    ChangePassword.objects.filter(user=request.user).delete()
    return redirect('view')

def isValid(s):
    Pattern = re.compile("(0/91)?[6-9][0-9]{9}")
    return Pattern.match(s)
