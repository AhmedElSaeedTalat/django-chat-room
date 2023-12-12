from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.


def home(request):
    """ home page """
    return render(request, 'index.html')

def room(request, room_name):
    return render(request, 'room.html', {'room_name': room_name})
