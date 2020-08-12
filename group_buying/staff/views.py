from django.shortcuts import render
from dealer.models import Dealer
from profiles.models import UserProfile
# Create your views here.
def confirm(request):
    objs = Dealer.objects.filter(kyc_verified=False).values()
    print(objs)
    return render(request,'staff/confirm.html')
