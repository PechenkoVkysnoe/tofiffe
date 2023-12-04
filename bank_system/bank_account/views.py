import datetime
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from bank_account.forms import MakeBankAccountForm, MakeCreditCardForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, View
from bank_account.models import BankAccount, CreditCard
from accounts.utils import LoginConfirmedRequiredMixin


class BankAccountView(LoginConfirmedRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        bank_accounts = BankAccount.objects.filter(user=request.user)
        credit_cards = CreditCard.objects.filter(bank_account__user=request.user)
        context = {
            'bank_accounts': bank_accounts,
            'credit_cards': credit_cards
        }
        return render(request, 'bank_account/base.html', context)


class MakeBankAccount(LoginConfirmedRequiredMixin, CreateView):
    model = BankAccount
    form_class = MakeBankAccountForm
    success_url = reverse_lazy('bank-account')
    template_name = 'bank_account/make_bank_account.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = random.randint(1000, 9999)
        return super().form_valid(form)


class MakeCreditCard(LoginConfirmedRequiredMixin, CreateView):
    model = CreditCard
    form_class = MakeCreditCardForm
    success_url = reverse_lazy('bank-account')
    template_name = 'bank_account/make_credit_card.html'

    def form_valid(self, form):
        form.instance.number = '1234'
        form.instance.cvv = random.randint(100, 999)
        form.instance.date_to = datetime.date.today() + datetime.timedelta(days=365*3 + 366)
        form.instance.owner_name = form.cleaned_data['owner_name'].upper()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
