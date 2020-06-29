from django.http import  HttpResponseNotAllowed
from django.db import IntegrityError
from django.shortcuts import render, redirect,reverse
from .models import ChatRoom, ChatMessage
from django.http import HttpResponseRedirect,HttpResponse
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
            # response = '<html><script>alert("Enter valid amount");window.location=/rooms/' + str(room_id) + '"";</script></html>'
            print(path)

            return HttpResponseRedirect(path)
            # return H
        ChatMessage.objects.create(room=room,user=mfrom,text=text,document=file,image=img)

        # try:
        #     ChatMessage.objects.create(room=room,user=mfrom,text=text,image=img)
        # except:
        #     try:
        #         ChatMessage.objects.create(room = room,user=mfrom,text=text,file = file)
        #     except:
        #         try:
        #             ChatMessage.objects.create(room=room,user=mfrom,text=text)
        #         except:
        #             return HttpResponse('you need to enter any of the following : message or image or file')
        return redirect('home',room_id=room_id)
    else:
        return HttpResponseNotAllowed(['POST'])


def delete(request,room,id):
    ChatMessage.objects.filter(id=id).delete()
    return redirect('home', room_id=room)

