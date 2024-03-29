from django.shortcuts import render

from chatapp.models import Room
# Create your views here.


def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })

def room_view(request, room_name):
    chatapp_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chatapp_room,
    })
