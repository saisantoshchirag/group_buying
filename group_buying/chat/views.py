from django.http import  HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import ChatRoom, ChatMessage,ChatUser
from django.http import HttpResponseRedirect,HttpResponse
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required


def home(request, room_id):
    user = UserProfile.objects.filter(user=request.user).values()
    if not room_id == str(user[0]['room_id']):
        return HttpResponse('<html><script>alert("You are not part of this room. Please join you own room");window.location="/chat";</script></html>')
    if user:
        try:
            result = {}
            room = ChatRoom.objects.get(eid=room_id)
            chat_users = ChatUser.objects.filter(chat=room).values()
            print(chat_users)
            usernames = []
            for i in range(len(chat_users)):
                userss = User.objects.filter(id=chat_users[i]['user_id']).values()
                print(userss)
                usernames.append(userss[0]['username'])
                print(chat_users[i])
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
        print(user)
        print(room_id)
        print(type(user[0]['room_id']))
        print(type(room_id))
        print(user==room_id)
        if not room_id==str(user[0]['room_id']):
            return HttpResponse('<html><script>alert("You are not part of this room. Please join you own room");window.location="/chat";</script></html>')

        mfrom = request.POST['from']
        if not any(fields):
            return HttpResponseRedirect(path)
        ChatMessage.objects.create(room=room,user=mfrom,text=text,document=file,image=img)
        return redirect('home',room_id=room_id)
    else:
        return HttpResponseNotAllowed(['POST'])


def delete(request,room,id):
    ChatMessage.objects.filter(id=id).delete()
    return redirect('home', room_id=room)

@login_required(login_url='/loginmodule/login/')
def rooms(request):
    userprofile = UserProfile.objects.filter(user=request.user).values()
    if len(userprofile) == 0:
        return redirect('create')
    room = UserProfile.objects.filter(user=request.user).values()[0]['room_id']
    if room is None:
        room = ''
    rooms = ChatRoom.objects.all().values()
    user = User.objects.filter(username=request.user)
    is_staff = user.values()[0]['is_staff']
    return render(request,'chat/rooms.html',{'rooms':rooms,'is_staff':is_staff,'room_user':room})


def join(request,room_id):
    try:
        userprofile = UserProfile.objects.filter(user=request.user).values()
    except:
        return redirect('create')
    rooms = ChatRoom.objects.filter(eid=room_id)
    UserProfile.objects.filter(user=request.user).update(room=room_id)
    ChatUser.objects.create(chat=rooms[0],user=request.user)
    return redirect('home',room_id=room_id)