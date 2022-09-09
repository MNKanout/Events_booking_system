#Django modules
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib import messages
# Project modules
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm

def register(request):
    if request.method != "POST":
            if request.user.is_authenticated:
                return redirect('events_registry:events')
            else:
                form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            dj_login(request, new_user)
            return redirect('events_registry:events')

        else:
            messages.add_message(request, messages.ERROR,'Registering faild!',extra_tags='danger')


    context = {'form':form}
    return render(request, "register.html",context)


def login(request):
    if request.method != 'POST':
        if request.user.is_authenticated:
            return redirect('events_registry:events')
        else:
            form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                dj_login(request, user)
                return redirect("events_registry:events")
        
        else:
            messages.add_message(request, messages.ERROR,'Login faild!',extra_tags='danger')

    context = {'form':form}
    return render(request,'login.html',context)
        

def logout(request):
    dj_logout(request)
    return redirect('events_registry:index')