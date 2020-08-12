from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Dealer
from profiles.models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def status(request):
    user = User.objects.filter(username=request.user).values()[0]['id']
    dealer = Dealer.objects.filter(user=user)
    if dealer:
        return redirect('dealer:current')
    return render(request,'dealer/status.html')

def upload(request):
    if request.method=='POST':
        print(request.FILES)
        user = User.objects.filter(username=request.user).values()[0]['id']

        profile = UserProfile.objects.get(user=user)
        print(request.FILES)
        aadhar = request.FILES['aadhar']
        pad = request.FILES['pan']
        gts = request.FILES['gts']
        reg = request.FILES['registration']
        manager = request.POST['manager']
        manager_mob = request.POST['manager_mobile']
        manager_email = request.POST['manager_email']
        bankname = request.POST['bankname']
        acc_no = request.POST['acc_no']
        acc_type = request.POST['acc_type']
        ifsc = request.POST['ifsc']
        Dealer.objects.create(user=request.user,profile=profile,aadhar=aadhar,pan=pad,gts=gts,registration=reg,manager=manager,manage_mobile=manager_mob,manager_email=manager_email,bank_name=bankname,account_number=acc_no,account_type=acc_type,ifsc_code=ifsc)
    return redirect('dealer:current')

def current(request):
    status = Dealer.objects.filter(user=request.user).values()[0]['kyc_verified']
    # print(status[0]['kyc_verified'])
    return render(request,'dealer/current.html',{'status':status})

def update(request):
    if request.method=='POST':
        user = User.objects.filter(username=request.user).values()[0]['id']
        try:
            aadhar = request.FILES['aadhar']
            Dealer.objects.filter(user=user).update(aadhar=aadhar)
        except:
            pass
        try:
            pan = request.FILES['pan']
            Dealer.objects.filter(user=user).update(pan=pan)
        except:
            pass
        try:
            gts = request.FILES['gts']
            Dealer.objects.filter(user=user).update(pan=gts)
        except:
            pass
        try:
            reg = request.FILES['registration']

            Dealer.objects.filter(user=user).update(registration=reg)
        except:
            pass
        try:
            manager = request.POST['manager']
            if len(manager)>0:

                Dealer.objects.filter(user=user).update(manager=manager)
            print(manager)
        except:
            pass
        try:
            manager_mob = request.POST['manager_mobile']
            Dealer.objects.filter(user=user).update(manager_mobile=manager_mob)
        except:
            pass
        try:
            manager_email = request.POST['manager_email']
            Dealer.objects.filter(user=user).update(manager_email=manager_email)
        except:
            pass
        try:
            bank = request.POST['bankname']
            if len(bank)>0:

                Dealer.objects.filter(user=user).update(bank_name=bank)
            print(bank)
        except:
            pass
        try:
            acc_no = request.POST['acc_no']
            Dealer.objects.filter(user=user).update(account_number=acc_no)
            print(acc_no)
        except:
            pass
        try:
            acc_type = request.POST['acc_type']
            if len(acc_type)>0:

                Dealer.objects.filter(user=user).update(account_type=acc_type)
            print(acc_type)
        except:
            pass
        try:
            ifsc = request.POST['ifsc']
            if len(ifsc)>0:
                Dealer.objects.filter(user=user).update(ifsc_code=ifsc)
            print(ifsc)
        except:
            pass
        return redirect('dealer:current')
    return render(request,'dealer/update.html')