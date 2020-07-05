from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UpdateForm
from django.core.files.storage import FileSystemStorage

# Create your views here

def update(request):

    current_user = UserProfile.objects.filter(user=request.user).values()
    cur_gender = current_user[0].get('gender')
    cur_state = current_user[0].get('state')
    cur_pincode = current_user[0].get('pincode')
    cur_city = current_user[0].get('city')
    cur_phone = current_user[0].get('phone_number')
    print(cur_city)
    print(cur_pincode)
    print(cur_state)
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
            # UserProfile.objects.filter(user=request.user).update(image=request.FILES['image'],state=request.POST['state'],phone_number=request.POST['phone_number'],city=request.POST['city'],pincode=request.POST['pincode'],gender=request.POST['gender'])
            try:
                UserProfile.objects.filter(user=request.user).update(phone_number=request.POST['phone_number'])
            except:
                UserProfile.objects.filter(user=request.user).update(phone_number=cur_phone)
            try:
                UserProfile.objects.filter(user=request.user).update(gender=request.POST['gender'])
            except:
                UserProfile.objects.filter(user=request.user).update(gender=cur_gender)
            try:
                print('coty if')
                UserProfile.objects.filter(user=request.user).update(city=request.POST['city'])
            except:
                print('cty else')
                UserProfile.objects.filter(user=request.user).update(city=cur_city)
            try:
                print('sta if')
                UserProfile.objects.filter(user=request.user).update(state=request.POST['state'])
                print(request.POST['state'])
                print('request')

            except:
                print('sta el')
                UserProfile.objects.filter(user=request.user).update(state=cur_state)
            try:
                print('pin if')
                UserProfile.objects.filter(user=request.user).update(pincode=request.POST['pincode'])
                print(request.POST['pincode'])

                print('request')

            except:
                print('pin else')
                UserProfile.objects.filter(user=request.user).update(pincode=cur_pincode)

            return redirect('view')
    else:
        form = UpdateForm()
    return render(request,'profiles/update.html',{'form':form})

def profile(request):
    user = UserProfile.objects.filter(user=request.user).values()
    if not user:
        return redirect('create')
    return render(request,'profiles/profile.html',{'user':request.user})

def create(request):
    if request.method == 'POST':
        pincode = request.POST.get('pincode')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        gender = request.POST.get('gender')
        image = request.FILES['image']
        UserProfile.objects.create(image = image,state=state,city=city,gender=gender,pincode=pincode,phone_number=phone_number,user=request.user)
        return redirect(request.GET.get('next','view'))
    return render(request,'profiles/create.html')
