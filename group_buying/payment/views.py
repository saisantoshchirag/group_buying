from django.shortcuts import render

# Create your views here.
def payment_home(request):
    return render(request,'payment/home.html')