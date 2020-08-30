from django.http import  HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import ChatRoom, ChatMessage,ChatUser
from django.http import HttpResponseRedirect,HttpResponse
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages as Messgs
import datetime


def home(request, room_id):
    user = UserProfile.objects.filter(user=request.user).values()
    print(user)
    use1 = UserProfile.objects.filter(user=request.user,subscription_end__gte=datetime.datetime.now()).values()
    print('entered room',room_id)
    print('joined rooms',user[0]['joined'])
    print('bool',int(room_id) in user[0]['joined'])
    if int(room_id) not in user[0]['joined']:
        return HttpResponse('<html><script>alert("You are not part of this room. Please join you own room");window.location="/chat";</script></html>')
    if not user[0]['is_subscribed']:
        return redirect('payment:Checkout')
    # if user[0]['subscription_end']<datetime.datetime.now():
    try:
        subs =  use1[0]
    except:
        UserProfile.objects.filter(user=request.user).update(is_subscribed=False)
        Messgs.success(request,'Sub ended renew')
        return redirect('payment:Checkout')
    if user:
        try:
            result = {}
            room = ChatRoom.objects.get(id=room_id)
            chat_users = ChatUser.objects.filter(chat=room).values()
            usernames = []
            for i in range(len(chat_users)):
                userss = User.objects.filter(id=chat_users[i]['user_id']).values()
                usernames.append(userss[0]['username'])
                # print(chat_users[i])

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
        return render(request, 'chat/chat.html', {'context':context1,'username':usernames})
    else:
        context = {}
        context['room_id'] = room_id or 'default'
        return render(request, 'chat/join.html', {'context':context,'context1':context})
def messages(request, room_id):
    if request.method == 'POST':
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
        try:
            room = ChatRoom.objects.get(eid=room_id)
        except ChatRoom.DoesNotExist:
            return HttpResponse('room doesnot exist')
        user = UserProfile.objects.filter(user=request.user).values()
        if not room_id==str(user[0]['room_id']):
            return HttpResponse('<html><script>alert("You are not part of this room. Please join you own room");window.location="/chat";</script></html>')
        mfrom = request.POST['from']
        if not any(fields):
            return HttpResponseRedirect(path)
        ChatMessage.objects.create(room=room,user=mfrom,text=text,document=file,image=img)
        return redirect('chat:home',room_id=room_id)
    else:
        return HttpResponseNotAllowed(['POST'])


def delete(request,room,id):
    ChatMessage.objects.filter(id=id).delete()
    return redirect('chat:home', room_id=room)

@login_required(login_url='/loginmodule/login/')
def rooms(request):
    userprofile = UserProfile.objects.filter(user=request.user).values()
    if len(userprofile) == 0:
        return redirect('create')
    room = UserProfile.objects.filter(user=request.user).values()[0]['room_id']
    joined_rooms = UserProfile.objects.filter(user=request.user).values()[0]['joined']
    # print(rooms)
    print(room)
    if room is None:
        room = ''
    rooms = ChatRoom.objects.all().values()
    user = User.objects.filter(username=request.user)
    # use = UserProfile.objects.filter(user=request.user).update(joined=[])
    print(rooms)
    print(joined_rooms)
    is_staff = user.values()[0]['is_staff']
    return render(request,'chat/rooms.html',{'rooms':rooms,'is_staff':is_staff,'room_user':joined_rooms})


def join(request,room_id):
    try:
        userprofile = UserProfile.objects.filter(user=request.user).values()
    except:
        return redirect('create')
    if not userprofile[0]['is_subscribed']:
        return redirect('payment:Checkout')
    is_user_joined = ChatUser.objects.filter(user=request.user)
    if len(is_user_joined)>0:
        Messgs.success(request,'You already in a room.')
        return redirect('chat:rooms')
    rooms = ChatRoom.objects.filter(eid=room_id)
    UserProfile.objects.filter(user=request.user).update(room=room_id,joined=[room_id])

    ChatUser.objects.create(chat=rooms[0],user=request.user)
    return redirect('chat:home',room_id=room_id)

def create_room(request):
    id = 0
    for i in ChatRoom.objects.all().values():
        id = max(id, i['id'])
    if request.method == 'POST':
        vehicle = request.POST['vehicle']
        brand = request.POST['brand']
        limit = request.POST['limit']
        location = request.POST['location']
        name = vehicle + ' ' + brand + ' ' + location
        ChatRoom.objects.create(eid=id+1,name=name,max_limit = limit,location=location,brand = brand,vehicle=vehicle)
        rooms = ChatRoom.objects.filter(eid=id+1)
        ChatUser.objects.create(chat=rooms[0], user=request.user)
        joined_rooms = UserProfile.objects.get(user=request.user).joined
        joined_rooms.append(id+1)
        UserProfile.objects.filter(user=request.user).update(joined=joined_rooms)
        return redirect('chat:rooms')
    return render(request,'chat/create.html',{'id':id+1})