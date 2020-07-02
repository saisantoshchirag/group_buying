from django.http import  HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,reverse
from .models import ChatRoom, ChatMessage,Car
from django.http import HttpResponseRedirect,HttpResponse
import pandas as pd
from profiles.models import UserProfile
def home(request, room_id=None):
    user = request.user
    if user:
        if not room_id:
            return redirect('/default?' + request.GET.urlencode())
        try:
            result = {}
            room = ChatRoom.objects.get(eid=room_id)
            cmsgs = ChatMessage.objects.filter(
                room=room).order_by('date')[:50].values()
            msgs = []
            for msg in cmsgs:
                msg['is_delete'] = str(request.user)==msg['user']
                cur_date = msg['date'].strftime('%b %d %Y')
                if cur_date not in result:
                    result[cur_date] = []
                result[cur_date].append(msg)
                msgs.append(msg)
        except ChatRoom.DoesNotExist:
            msgs = []
        context1 = {}
        context1['room_id'] = room_id
        context1['messages'] = result
        context1['user'] = user
        return render(request, 'chat/chat.html', {'context':context1})
    else:
        context = {}
        context['room_id'] = room_id or 'default'
        return render(request, 'chat/join.html', {'context':context,'context1':context})
def messages(request, room_id):
    if request.method == 'POST':
        fields = []
        try:
            img = request.FILES['image']
        except:
            img = None
        try:
            text = request.POST['text']
        except:
            text = None
        try:
            file = request.FILES['file']
        except:
            file = None

        path = request.POST['next']
        fields = [img,file,text]
        print(fields)
        try:
            room = ChatRoom.objects.get(eid=room_id)
        except ChatRoom.DoesNotExist:
            return HttpResponse('room doesnot exist')

        mfrom = request.POST['from']
        if not any(fields):
            print(path)
            return HttpResponseRedirect(path)
        ChatMessage.objects.create(room=room,user=mfrom,text=text,document=file,image=img)
        return redirect('home',room_id=room_id)
    else:
        return HttpResponseNotAllowed(['POST'])


def delete(request,room,id):
    ChatMessage.objects.filter(id=id).delete()
    return redirect('home', room_id=room)

def rooms(request):
    rooms = ChatRoom.objects.all().values()
    cars = Car.objects.all().values()
    user = User.objects.filter(username=request.user)
    is_staff = user.values()[0]['is_staff']
    res = []
    for i in rooms:
        out = {}
        for j in cars:
            if i['id']==j['id']:
                out = i
                out.update(j)
                res.append(out)
    return render(request,'chat/rooms.html',{'rooms':res,'is_staff':is_staff})

#THis view if for adding more cars to database
def data(request):
    file = pd.read_csv('C:\sem-6\group_buying\group_buying\chat\Book1.csv')
    print(file.columns)
    for i in range(len(file['id'])):
        Car.objects.create(name=file['Modelname'][i],brand = file['Brand'][i],version=file['Version'][i],price=file['Price'][i],mileage=file['Milage'][i],fuel_tank_capacity=file['Fuel_tank_capacity'][i],fuel_type=file['Fueltype'],body_style=file['Body_style'])
    return HttpResponse('success')

def join(request,room_id):
    # print(room_id)
    user = User.objects.filter(username=request.user)
    user1 = UserProfile.objects.filter(user=request.user)
    print(user)
    print(user1)
    return HttpResponse('here')