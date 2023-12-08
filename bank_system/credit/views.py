import calendar
import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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


def make_credit_transactions(credit):
    if credit.credit.type == CreditType.objects.get(type='Аннуитетный'):
        # константы из формулы 3/4 лабы
        i = credit.credit.percent
        n = credit.credit.period_in_month
        k = (i / 1200 * ((1 + i / 1200) ** n)) / ((1 + i / 1200) ** n - 1)
        current_date = datetime.datetime.now()
        mouth_now = current_date.month
        year_now = current_date.year
        for _ in range(1, credit.credit.period_in_month + 1):
            mouth_now += 1
            if mouth_now == 13:
                mouth_now = 1
                year_now += 1
            CreditTransaction.objects.create(
                dt=datetime.datetime(year_now, mouth_now, 1, 0, 0, 1),
                amount=float(credit.amount) * k,
                credit=credit
            )


class MyCreditView(View):
    def get(self, request, *args, **kwargs):
        credits = UserCredit.objects.filter(bank_account__user=request.user)
        context = {
            'credits': credits
        }
        return render(request, 'bank_account/my_credit.html', context)


class CreateCreditView(LoginRequiredMixin, CreateView):
    model = CardTransaction
    form_class = CreateCreditForm
    template_name = 'credit/make_credit.html'
    success_url = reverse_lazy('my-credit')

    def form_valid(self, form):
        credit = form.cleaned_data['credit']
        bank_account = form.cleaned_data['bank_account']

        if BankAccount.objects.filter(name=bank_account).first().currency != Credit.objects.filter(name=credit).first().currency:

            messages.success(self.request, "Ваша заявка на кредит НЕ принята. Валюты банковского счета и кредита разные!")
            return super().form_valid(form)
        form.instance.credit = credit
        form.instance.bank_account = bank_account
        form.instance.status = CreditStatus.objects.get(name='В ожидании')
        form.instance.amount = form.cleaned_data['amount']

        credit = form.save()
        make_credit_transactions(credit)
        messages.success(self.request, "Ваша заявка на кредит принята, ожидайте!")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
