import calendar
import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from transaction.models import CardTransaction, TransactionStatus, TransactionType


from credit.forms import CreateCreditForm

from credit.models import CreditStatus

from credit.models import CreditTransaction, CreditType

from credit.models import UserCredit

from bank_account.models import BankAccount

from credit.models import Credit

from deposit.models import UserDeposit

from deposit.forms import CreateDepositForm

from deposit.models import Deposit


class MyDepositView(View):
    def get(self, request, *args, **kwargs):
        deposits = UserDeposit.objects.filter(bank_account__user=request.user)
        context = {
            'deposits': deposits
        }
        return render(request, 'bank_account/my_deposit.html', context)


class CreateDepositView(LoginRequiredMixin, CreateView):
    model = CardTransaction
    form_class = CreateDepositForm
    template_name = 'deposit/make_deposit.html'
    success_url = reverse_lazy('my-deposit')

    def form_valid(self, form):
        deposit = form.cleaned_data['deposit']
        bank_account = BankAccount.objects.filter(name=form.cleaned_data['bank_account']).first()
        amount = form.cleaned_data['amount']

        if bank_account.currency != Deposit.objects.filter(name=deposit).first().currency:
            messages.success(self.request, "Ваша заявка на депозит НЕ принята. Валюты банковского счета и депозита разные!")
            return HttpResponseRedirect('/bank-account/my-deposit/')
        if bank_account.balance < amount:
            messages.success(self.request, "Ваша заявка на депозит НЕ принята. На указаном счете недостаточно средств!")
            return HttpResponseRedirect('/bank-account/my-deposit/')
        if bank_account.account_type.type == 'Сберегательный':
            messages.success(self.request, "Ваша заявка на депозит НЕ принята. Нельзя списывать с сберегательного счета!")
            return HttpResponseRedirect('/bank-account/my-deposit/')

        bank_account.balance -= amount
        bank_account.save()

        form.instance.deposit = deposit
        form.instance.bank_account = bank_account
        form.instance.amount = amount

        messages.success(self.request, "Ваш депозит успешно создан!")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
