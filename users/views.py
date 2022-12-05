from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import User
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import logout


def home(request):
    return render(request, 'users/home.html')

def UserRegistration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)

@csrf_exempt
def UserLogin(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
           
            
            login(request, user)

            return redirect('movies')
        else:
            return redirect('login')
    
    return render(request, 'users/login.html')   


def UserLogout(request):
    print("logout")
    logout(request)
    return redirect('movies')
    
