from django.shortcuts import render

# Create your views here.
def update(request):
    return render(request,'profiles/update.html')