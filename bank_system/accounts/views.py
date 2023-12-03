from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from accounts.forms import LoginForm, RegisterForm
from hashlib import sha256
import hmac
from accounts.utils import verify_telegram_authentication
from accounts.models import User


TELEGRAM_BOT_TOKEN = '6510492757:AAGSxkG85ynW3C4EFN0bKjIvFedE_0kIKRE'

def index(request):
    if request.user.is_authenticated and request.user.telegram_id == 0:
        return redirect('register_telegram')

    return render(request, 'users/index.html')

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.telegram_id = 0
            user.save()
            messages.success(request, 'Now please, connect your telegram to ensure more security.')
            login(request, user)
            return redirect('register_telegram')
        else:
            return render(request, 'users/register.html', {'form': form})


def sign_up_telegram(request):
    if request.method == 'GET':
        if request.user and request.user.telegram_id == 0:
            if request.GET.get('hash'):
                if verify_telegram_authentication(TELEGRAM_BOT_TOKEN, request.GET):
                    user = User.objects.filter(id=request.user.id)

                    if user:
                        user = user[0]
                        user.telegram_id = int(request.GET.get('id')) 
                        user.save()
                        messages.success(request,f'Telegram id successfully linked!')
                        return redirect('index')

            return render(request, 'users/register_telegram.html')

    
def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')
        
        if request.GET.get('hash'):
            if verify_telegram_authentication(TELEGRAM_BOT_TOKEN, request.GET):
                user = User.objects.filter(telegram_id=int(request.GET.get('id')))

                if user:
                    user = user[0]
                    login(request, user)
                    messages.success(request,f'Hi {user.first_name}, welcome back!')
                    return redirect('index')
        
        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('index')
    
        # either form not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'users/login.html',{'form': form})


def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')     