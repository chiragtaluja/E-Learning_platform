from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, User, Message
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import get_backends


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password is incorrect")

    context = {"page": page}

    return render(request, "base/login_register.html", context)


def RegisterUser(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)

            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")

    context = {"form": form}
    return render(request, "base/login_register.html", context)


def home(request):
    q = request.GET.get("q", "")
    if q:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q)
            | Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(host__username__icontains=q)
        )
    else:
        rooms = Room.objects.all()
    topics = Topic.objects.all()
    room.messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    room_count = rooms.count()
    context = { 
        "rooms": rooms,
        "topics": topics,
        "recent_messages": room.messages[:5],
        "room_count": room_count,
    }
    return render(request, "base/home.html", context)


def room(request, room_id):
    room = Room.objects.get(id=room_id)
    room_messages = room.message_set.all().order_by("-created")
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body"),
            created=request.POST.get("created"),
        )
        room.participants.add(request.user)
        message.save()

        return redirect("room", room_id=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
        "message": Message(),
        "form": RoomForm(),
    }
    return render(request, "base/room.html", context)


@login_required(login_url="/login")
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        form.instance.host = request.user

        if form.is_valid():
            form.save()
            return redirect("home")
    context = {
        "form": form,
    }
    return render(request, "base/create_room.html", context)


@login_required(login_url="/login")
def update_room(request, room_id):
    room = Room.objects.get(id=room_id)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {
        "form": form,
    }
    return render(request, "base/create_room.html", context)


@login_required(login_url="/login")
def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        room.delete()
        return redirect("home")

    context = {
        "room": room,
    }
    return render(request, "base/delete_room.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def delete_message_room(request, message_id):
    message = Message.objects.get(id=message_id)

    if request.user != message.user:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        message.delete()
        return redirect("room", room_id=message.room.id)

    context = {
        "message": message,
    }
    return render(request, "base/room.html", context)


def profile(request, username):
    profile_user = User.objects.get(username=username)
    recent_messages = Message.objects.filter(user=profile_user).order_by("-created")[:5]
    topics = Topic.objects.all()
    rooms = Room.objects.filter(host=profile_user)
    context = {
        "recent_messages": recent_messages,
        "profile_user": profile_user,
        "username": username,
        "topics": topics,
        "rooms": rooms,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="/login")
def add_topics(request):
    if request.method == "POST":
        topic_name = request.POST.get("topic_name")
        if topic_name:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            if created:
                messages.success(request, f"Topic '{topic_name}' added successfully!")
            else:
                messages.info(request, f"Topic '{topic_name}' already exists.")
        else:
            messages.error(request, "Topic name cannot be empty.")
    return redirect("home")


@login_required(login_url="/login")
def update_user(request, username):
    user = User.objects.get(username=username)
    form = UserForm(instance=user)
    if request.user != user:
        return HttpResponse("You are not allowed here!")
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", username=user.username)

    context = {
        "form": form,
    }
    return render(request, "base/update_user.html", context)


def about_us(request):
    return render(request, "base/about_us.html")


def index(request):
    return render(request, "base/index.html")

def contact_us(request):
    return render(request, "base/contact_us.html")