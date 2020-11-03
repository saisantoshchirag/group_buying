from django.shortcuts import render,redirect
from .models import UserProfile,ChangePassword
from .forms import UpdateForm
import re
from django.contrib.auth.models import User
from twilio.rest import Client
from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/loginmodule/login/')
def update(request):
    current_user = UserProfile.objects.filter(user=request.user).values()
    cur_gender = current_user[0].get('gender')
    cur_state = current_user[0].get('state')
    cur_pincode = current_user[0].get('pincode')
    cur_city = current_user[0].get('city')
    if request.method == 'POST':
        print(request.POST)
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
            return redirect('view',name=request.user)
    else:
        form = UpdateForm()
    return render(request,'profiles/update.html',{'form':form})

@login_required(login_url='/loginmodule/login/')
def profile(request,name):
    user = User.objects.filter(username=name).values()
    userprofile = user[0]['id']
    user = UserProfile.objects.filter(user_id=userprofile).values()
    is_user = name==str(request.user)
    if not user and is_user:
        return redirect('create')
    if not user and not is_user:
        messages.success(request, 'Profile Doesnot exist')
        return redirect('home')
    return render(request,'profiles/profile.html',{'user':request.user,'is_user':is_user,'is_phone_verified':user[0]['phone_verified']})

@login_required(login_url='/loginmodule/login/')
def create(request):
    userprofile = UserProfile.objects.filter(user=request.user).values()
    if len(userprofile) > 0:
        return redirect('view',name=request.user)

    if request.method == 'POST':
        pincode = request.POST.get('pincode')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        gender = request.POST.get('gender')

        UserProfile.objects.create(state=state,city=city,gender=gender,pincode=pincode,phone_number=phone_number,user=request.user,phone_verified=False,joined=[])
        code = get_random_string(length=6, allowed_chars='0123456789')
        otps = ChangePassword.objects.filter(user=request.user)
        if otps:
            ChangePassword.objects.filter(user=request.user).delete()
        ChangePassword.objects.create(user=request.user, code=code, phone_number=phone_number)
        body = 'Please verify your phone number.OTP: ' + str(code) + '. Do not share with anyone!!!'
        send_otp(body,str(phone_number))
        return render(request,'profiles/otp.html')
    return render(request,'profiles/create.html')

def phone_number(request):
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
            messages.success(request,'You have entered your current phone number.Please enter another number!')
            return redirect('phone_number')
        if not isValid(phone):
            messages.success(request,'You have entered invalid phone number .Please check again!')
            return redirect('phone_number')
        code = get_random_string(length=6,allowed_chars='0123456789')
        otps = ChangePassword.objects.filter(user=request.user)
        if otps:
            ChangePassword.objects.filter(user=request.user).delete()
        ChangePassword.objects.create(user=request.user,code=code,phone_number=phone)
        body = 'Please verify your phone number.OTP: '+str(code) + '. Do not share with anyone!!!'
        send_otp(body,str(phone))
    return render(request,'profiles/otp.html')

def validate_otp(request):
    obj = ChangePassword.objects.filter(user=request.user).values()
    if request.POST['otp'] == str(obj[0]['code']):
        UserProfile.objects.filter(user=request.user).update(phone_number=obj[0]['phone_number'],phone_verified=True)
    ChangePassword.objects.filter(user=request.user).delete()
    return redirect('view',name=request.user)

def verify_phone(request):
    user = User.objects.filter(username=request.user).values()
    userprofile = user[0]['id']
    user = UserProfile.objects.filter(user_id=userprofile).values()
    code = get_random_string(length=6, allowed_chars='0123456789')
    otps = ChangePassword.objects.filter(user=request.user)
    phone = user[0]['phone_number']
    if otps:
        ChangePassword.objects.filter(user=request.user).delete()
    ChangePassword.objects.create(user=request.user, code=code, phone_number=phone)
    body = 'Please verify your phone number for NayaGaadi. OTP: ' + str(code) + '. Do not share with anyone!!!'
    send_otp(body,str(phone))
    return render(request,'profiles/otp.html')


def send_otp(message,phone):
    account_sid = 'ACc3334be22f266fb10c6ce4e77a660264'
    auth_token = 'a3857fb9e733d9f9303abfd04319c534'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_='+12058436831',
        to='+91' + str(phone)
    )
def isValid(s):
    Pattern = re.compile("(0/91)?[6-9][0-9]{9}")
    return Pattern.match(s)
