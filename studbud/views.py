from django.shortcuts import render , redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import * 
from .forms import *
# Create your views here.
def home(request):
    q = request.GET.get('q') if  request.GET.get('q') != None else ''
    Rooms = room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = Rooms.count()
    Messages = message.objects.filter(Q(room__topic__name__icontains=q))[0:5]
    context = {
        'Rooms':Rooms ,
        'topics':topics,
        "room_count":room_count,
        "Messages":Messages
    }
    return render(request , "studbud/home.html" , context)

def ROOM(request , pk):
    Room = room.objects.get(id = pk)
    Room_messages = Room.message_set.all()
    participants = Room.participants.all()
    if request.method == 'POST':
        Message = message.objects.create(
            user =request.user,
            room =Room,
            body = request.POST.get('body') 
        )
        Room.participants.add(request.user)
        return redirect('room' , pk=Room.id)
    context = {
        'Room':Room , 
        'Room_messages':Room_messages,
        'participants':participants
    }
    return render(request , "studbud/room.html" , context)

@login_required
def create_room(request):
    form = roomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = roomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name= topic_name)
        room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name') ,
            description = request.POST.get('description')
        )
        return redirect("home")
    
    context = {
        'form':form ,
        'topics':topics
    }
    return render(request , "studbud/createroom.html" , context )

@login_required
def editroom(request , pk):
    Room = room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = roomForm(instance=Room)
    if request.user != Room.host:
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name= topic_name)
        Room.name = request.POST.get('name') 
        Room.topic = topic
        Room.description = request.POST.get('description')
        Room.save()
        return redirect("home")
    
    context = {
        'form':form,
        'topics':topics , 
        'Room': Room
    }
    return render(request , "studbud/createroom.html" , context )

@login_required
def delete_room(request , pk):
    Room = room.objects.get(id = pk)
    if request.method =='POST':
        Room.delete()
        return redirect("home")
    return render (request , "studbud/deleteroom.html" , {'obj':Room} )

@login_required
def delete_message(request , pk):
    Message = message.objects.get(id = pk)

    if request.user != Message.user:
        return HttpResponse("You are not allowed here!")
    
    if request.method =='POST':
        Message.delete()
        return redirect("home")
    return render (request , "studbud/deleteroom.html" , {'obj':Message} )

def profile(request , pk):
    user = User.objects.get(id=pk)
    
    Rooms = user.room_set.all()
    Messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "topics":topics,
        "Rooms":Rooms,
        "Messages":Messages

    }
    return render(request , "studbud/profile.html" , context)

def logedin(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request , request.POST)
        if form.is_valid():
            username = request.POST['username'].lower()
            request.POST = request.POST.copy()
            request.POST['username'] = username
            user = form.get_user()
            login (request  , user)
            return redirect('home')
        else:
            messages.error(request , "You entered wrong password or name!")
        

    else :
        form = AuthenticationForm()
    context= {
        'form':form,
        'page':page,
    }
    return render(request , 'studbud/login_register.html' , context)

def logedout(requset):
    logout(requset)
    return redirect('login')

def register(request):
    form = myUserCreationForm()
    if request.method == 'POST':
        form = myUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login (request  , user)
            return redirect('home')
        else:
            messages.error(request , "Something went wrong during registration!")
            
    
    context= {
        'form':form
    }
    return render(request , 'studbud/login_register.html' , context)

@login_required
def updateUser(request):
    users = request.user
    form = userForm(instance=users)

    if request.method == 'POST':
        form = userForm(request.POST, request.FILES, instance=users)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=users.id)

    return render(request, 'studbud/update-user.html', {'form': form})

def topics(request):
    q = request.GET.get('q') if  request.GET.get('q') != None else ''
    topicss = Topic.objects.filter(name__icontains=q)
    return render (request , 'studbud/topics.html' , {'topicss':topicss})

def activity(request ):
    
    Messages = message.objects.all()
    return render (request , 'studbud/activity.html' , {'Messages':Messages})
