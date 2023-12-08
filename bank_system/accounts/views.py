import datetime
import decimal
import threading
from time import sleep
from functools import wraps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from accounts.forms import LoginForm, RegisterForm
from django.views.generic.edit import View
from bank_account.models import CurrencyRelation
from accounts.utils import verify_telegram_authentication
from accounts.models import User
from deposit.models import UserDeposit

from credit.models import UserCredit
from credit.models import CreditTransaction

TELEGRAM_BOT_TOKEN = '6510492757:AAGSxkG85ynW3C4EFN0bKjIvFedE_0kIKRE'

C = 0


class Index(View):
    def get(self, request, *args, **kwargs):
        def f():
            last = []
            while True:
                month = datetime.datetime.now().month
                year = datetime.datetime.now().year

                if last != [year, month]:
                    last = [year, month]
                    deposits = UserDeposit.objects.all()
                    for deposit in deposits:
                        percent = deposit.deposit.percent
                        deposit.amount += decimal.Decimal(((1 + percent / 100) * float(deposit.amount)) ** (1 / 12))
                        deposit.save()
                    credits = UserCredit.objects.all()
                    for credit in credits:
                        sum_add = decimal.Decimal(0)
                        transactions = CreditTransaction.objects.filter()
                        for transaction in transactions:
                            # assert 1 == 2, transaction.dt.month
                            m = int(str(transaction.dt.date())[5:7])
                            y = int(str(transaction.dt.date())[:4])

                            if m * 12 + y <= last[0] * 12 + last[1]:
                                sum_add += decimal.Decimal(transaction.amount * decimal.Decimal(0.1))
                                transaction.amount *= decimal.Decimal(0.1)
                                transaction.save()
                        credit.amount += decimal.Decimal(sum_add)
                        credit.save()

                sleep(86400)

        global C
        if C == 0:
            C += 1
            threading.Thread(target=f, daemon=True).start()
        if request.user.is_authenticated:
            if request.user.telegram_id == 0:
                return redirect('register_telegram')
            if not request.user.confirmed:
                return redirect('await_confirm')

        currency_relations = CurrencyRelation.objects.all()
        context = {
            'currency_relations': currency_relations
        }
        return render(request, 'users/index.html', context=context)


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
        if request.user.is_authenticated:
            if request.user.telegram_id == 0:
                if request.GET.get('hash'):
                    if verify_telegram_authentication(TELEGRAM_BOT_TOKEN, request.GET):
                        user = User.objects.filter(id=request.user.id)

                        if user:
                            user = user[0]
                            user.telegram_id = int(request.GET.get('id'))
                            user.save()
                            messages.success(request, f'Telegram id successfully linked!')
                            return redirect('index')

                return render(request, 'users/register_telegram.html')
            else:
                return redirect("index")
        else:
            return redirect("login")


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
                    messages.success(request, f'Hi {user.first_name}, welcome back!')
                    return redirect('index')

        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
        # either form not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'users/login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('login')


class AwaitConfirm(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            if request.user.telegram_id == 0:
                return redirect("register_telegram")
            if request.user.confirmed:
                return redirect("index")
        return render(request, 'users/await_confirm.html')
