from django.shortcuts import render,redirect
from dealer.models import Dealer
from profiles.models import UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.models import User
# Create your views here.
def confirm(request):
    total = []
    objs = Dealer.objects.filter(kyc_verified=False).values()
    for i in objs:
        uid = i['user_id']
        user = User.objects.filter(id=uid).values()[0]['username']
        print(user)
        userprofile = UserProfile.objects.filter(user=uid).values()
        i['username'] = user
    print(objs)
    return render(request,'staff/confirm.html',{'total':objs})

def update_status(request,user_id,status):
    if status=='Accept':
        dealer = Dealer.objects.filter(user=user_id).update(kyc_verified=True)
        UserProfile.objects.filter(user_id=user_id).update(is_dealer=True)
        UserProfile.objects.filter(user_id=user_id).update(is_user=False)
    return redirect(request,'staff:update_status')