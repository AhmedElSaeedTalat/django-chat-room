from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import AsyncToSync
import json
import redis
# Create your views here.

def home(request):
    """ home page """
    return render(request, 'index.html', {'request': request})

def room(request, room_name):
    """ return room for the chat """
    return render(request, 'room.html', {'room_name': room_name})

def register(request):
    """ function to register """
    if request.user.username:
        return redirect('home')
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['email'].split('@')[0]
            """ login user after saving new user """
            user = authenticate(
                username=username,
                password=form.cleaned_data['password1']
            )
            messages.success(request, 'Registration successful')
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, f"error") 
    return render(request, 'registration.html', {'form': form})

def logmein(request):
    """ view function to login in user """
    if request.user.username:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        username = email.split('@')[0]
        password = request.POST['password']
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'email or password is not correct')
    return render(request, 'login.html')

def logmeout(request):
    """ function to logout authenticated user """
    logout(request)
    return redirect('home')