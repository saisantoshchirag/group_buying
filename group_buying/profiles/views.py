from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UpdateForm
from django.core.files.storage import FileSystemStorage

# Create your views here

def update(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            UserProfile.objects.filter(user=request.user).update(image=request.FILES['image'],state=request.POST['state'],phone_number=request.POST['phone_number'],city=request.POST['city'],pincode=request.POST['pincode'],gender=request.POST['gender'])
            return redirect('view')
    else:
        form = UpdateForm()
    return render(request,'profiles/update.html',{'form':form})

def profile(request):
    user = UserProfile.objects.filter(user=request.user).values()
    return render(request,'profiles/profile.html',{'user':request.user})


def city(request):
    state = request.POST.get('state')
    city = request.POST.get('city')
    print(city)
    print(state)
    return  render(request,'profiles/cities.html')