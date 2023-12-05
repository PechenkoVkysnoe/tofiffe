import datetime
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from bank_account.forms import MakeBankAccountForm, MakeCreditCardForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, View
from bank_account.models import BankAccount, CreditCard, BankPartner

from transaction.models import Transaction


class BankAccountView(View):
    def get(self, request, *args, **kwargs):
        bank_accounts = BankAccount.objects.filter(user=request.user)
        credit_cards = CreditCard.objects.filter(bank_account__user=request.user)
        context = {
            'bank_accounts': bank_accounts,
            'credit_cards': credit_cards
        }
        return render(request, 'bank_account/base.html', context)


class MyBankAccountView(View):
    def get(self, request, *args, **kwargs):
        bank_accounts = BankAccount.objects.filter(user=request.user)
        context = {
            'bank_accounts': bank_accounts,
        }
        return render(request, 'bank_account/my_bank_account.html', context)


class MyCreditCardView(View):
    def get(self, request, *args, **kwargs):
        credit_cards = CreditCard.objects.filter(bank_account__user=request.user)
        context = {
            'credit_cards': credit_cards
        }
        return render(request, 'bank_account/my_credit_card.html', context)


class MyTransactionView(View):
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(credit_card_from__bank_account__user=request.user)
        context = {
            'transactions': transactions
        }
        return render(request, 'bank_account/my_transaction.html', context)


class MakeBankAccount(LoginRequiredMixin, CreateView):
    model = BankAccount
    form_class = MakeBankAccountForm
    success_url = reverse_lazy('my-bank-account')
    template_name = 'bank_account/make_bank_account.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = int(str(random.randint(1000, 9999)) + str(self.request.user.id))
        return super().form_valid(form)


class MakeCreditCard(LoginRequiredMixin, CreateView):
    model = CreditCard
    form_class = MakeCreditCardForm
    success_url = reverse_lazy('my-credit-card')
    template_name = 'bank_account/make_credit_card.html'

    def form_valid(self, form):
        form.instance.number = random.randint(100, 999)
        form.instance.cvv = random.randint(100, 999)
        form.instance.date_to = datetime.date.today() + datetime.timedelta(days=365*3 + 366)
        form.instance.owner_name = form.cleaned_data['owner_name'].upper()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PartnerView(View):
    def get(self, request, *args, **kwargs):
        bank_partners = BankPartner.objects.all()
        context = {
            'bank_partners': bank_partners,
        }
        return render(request, 'bank_account/partner.html', context)


class AboutUsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/about_us.html')
