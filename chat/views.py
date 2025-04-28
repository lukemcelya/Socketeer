from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # I'm just creating a default room that is created if it doesn't exist locally 
            general_room, created = Room.objects.get_or_create(name='general')
            general_room.users.add(user)

            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

def chat_room(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    room.users.add(request.user)

    all_rooms = Room.objects.all()

    messages = Message.objects.filter(room=room).order_by('timestamp')[:50]

    return render(request, "chat/base.html", {
        'room': room,
        'room_name': room_name,
        'rooms': all_rooms,
        'messages': messages,
})

def create_room(request):
    if request.method == "POST":
        print("POST DATA:", request.POST)
        room_name = request.POST.get('room_name')
        if room_name:
            room, created = Room.objects.get_or_create(name=room_name)
            room.users.add(request.user)
            return redirect('chat_room', room_name=room.name)
    return redirect('chat_home')