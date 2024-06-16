from django.shortcuts import render, get_object_or_404, redirect 
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from.models import *
from.forms import *
from django.contrib.auth.decorators import login_required
from .forms import AuthenticationForm
from django.contrib.auth import login
from .models import CustomUser
from django.db import IntegrityError
from django.contrib.auth.models import User




# Create your views here.

def index(request):
    return render(request, 'bigArt/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Account created successfully")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'bigArt/sign.html', {'form': form})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error_message = 'Invalid username or password'
    else:
        form = AuthenticationForm()
    return render(request, 'bigArt/login.html', {'form': form, 'error_message': error_message})


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('index')
        else:
            messages.error(request, 'There was an error in your form submission. Please correct the errors below.')
    else:
        form = ContactForm()
    
    return render(request, 'bigArt/contact.html', {'form': form})  

def about(request):
    return render(request, 'bigArt/about.html')






