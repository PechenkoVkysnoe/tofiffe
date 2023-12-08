import datetime
import random
from time import timezone

from django.http import HttpResponseRedirect
from faker import Faker
from django.shortcuts import render, redirect
from bank_account.forms import MakeBankAccountForm, MakeCreditCardForm, PayCreditForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, View, UpdateView
from bank_account.models import BankAccount, CreditCard, BankPartner

from transaction.models import CardTransaction
from accounts.utils import LoginConfirmedRequiredMixin
from credit.models import Credit
from bank_account.models import BankAccountType
from django.contrib import messages
from credit.models import CreditTransaction
from bank_account.models import CardTypePrivileges

from transaction.models import BankAccountTransaction

from bank_account.forms import PayDepositForm
from deposit.models import UserDeposit

from deposit.models import DepositTransaction

from credit.models import UserCredit


class BankAccountView(LoginConfirmedRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'bank_account/base.html')


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
        transactions_card = CardTransaction.objects.filter(credit_card_from__bank_account__user=request.user)
        transactions_account = BankAccountTransaction.objects.filter(bank_account_from__user=request.user)
        context = {
            'transactions_card': transactions_card,
            'transactions_account': transactions_account
        }
        return render(request, 'bank_account/my_transaction.html', context)


class MakeBankAccount(LoginConfirmedRequiredMixin, CreateView):
    model = BankAccount
    form_class = MakeBankAccountForm
    success_url = reverse_lazy('my-bank-account')
    template_name = 'bank_account/make_bank_account.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        account_type = form.cleaned_data['account_type']
        form.instance.account_type = account_type
        if account_type == BankAccountType.objects.filter(type='Обычный').first():
            type_number = '0001'
        else:
            type_number = '0002'
        user_number = str(self.request.user.id)
        check_number = int(type_number) + int(user_number)
        while (name := f'BY {str(check_number)} {random.randint(1000, 9999)} TOFI {type_number} {user_number}') in BankAccount.objects.values_list('name', flat=True):
            pass
        form.instance.name = name
        messages.success(self.request, "Ваш банковский аккаунт успешно создан!")
        return super().form_valid(form)


class MakeCreditCard(LoginConfirmedRequiredMixin, CreateView):
    model = CreditCard
    form_class = MakeCreditCardForm
    success_url = reverse_lazy('my-credit-card')
    template_name = 'bank_account/make_credit_card.html'

    def form_valid(self, form):
        while (number := Faker().credit_card_number(card_type='visa16')) in CreditCard.objects.values_list('number', flat=True):
            pass
        form.instance.number = number
        form.instance.cvv = random.randint(100, 999)
        form.instance.date_to = datetime.date.today() + datetime.timedelta(days=365*3 + 366)
        form.instance.owner_name = form.cleaned_data['owner_name'].upper()
        messages.success(self.request, "Ваша карта успешно создана!")
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


class CreditView(View):
    def get(self, request, *args, **kwargs):
        credits = Credit.objects.all()
        context = {
            'credits': credits,
        }
        return render(request, 'bank_account/credit.html', context)


class CardTypePrivilegesView(View):
    def get(self, request, *args, **kwargs):
        card_type_privileges = CardTypePrivileges.objects.all()
        context = {
            'card_type_privileges': card_type_privileges,
        }
        return render(request, 'bank_account/card_type_privileges.html', context)


class AboutUsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/about_us.html')


class CartTransactionView(View):
    def get(self, request, *args, **kwargs):
        number = kwargs.get('number')
        transaction_from = CardTransaction.objects.filter(credit_card_from=number)
        transaction_to = CardTransaction.objects.filter(credit_card_to=number)
        context = {
            'transaction_from': transaction_from,
            'transaction_to': transaction_to,
        }
        return render(request, 'bank_account/cart_transaction.html', context)


class BankAccoundTransactionView(View):
    def get(self, request, *args, **kwargs):
        number = kwargs.get('number')
        transaction_from = BankAccountTransaction.objects.filter(bank_account_from=number)
        transaction_to = BankAccountTransaction.objects.filter(bank_account_to=number)
        context = {
            'transaction_from': transaction_from,
            'transaction_to': transaction_to,
        }
        return render(request, 'bank_account/bank_account_transaction.html', context)


class CreditHistoryView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        credit_transactions = CreditTransaction.objects.filter(credit__id=id)
        context = {
            'credit_transactions': credit_transactions,
        }
        return render(request, 'bank_account/credit_transaction.html', context)


class PayView(LoginConfirmedRequiredMixin, UpdateView):
    form_class = PayCreditForm
    model = UserCredit
    template_name = 'credit/pay_credit.html'
    success_url = reverse_lazy('my-credit')

    def form_valid(self, form):
        credit = UserCredit.objects.filter(id=self.kwargs['pk']).first()
        amount = form.cleaned_data['amount']
        bank_account = BankAccount.objects.filter(name=form.cleaned_data['bank_account']).first()
        credit_transactions = CreditTransaction.objects.filter(credit=credit)
        if bank_account.balance < amount:
            messages.success(self.request, "На банковском счете недостаточно средств для оплаты!")
            return HttpResponseRedirect('/bank-account/my-credit/')
        if bank_account.currency != credit.credit.currency:
            messages.success(self.request, "Не возможно оплатить кредит, разные валюты!")
            return HttpResponseRedirect('/bank-account/my-credit/')

        paid_amount = 0
        for credit_transaction in credit_transactions:
            if credit_transaction.amount > 0:
                if credit_transaction.amount > amount:
                    paid_amount += amount
                    credit_transaction.amount -= amount
                    amount = 0
                else:
                    paid_amount += credit_transaction.amount
                    credit_transaction.amount = 0
                    amount -= credit_transaction.amount
            credit_transaction.save()

        bank_account.balance -= paid_amount
        bank_account.save()

        paid = True
        for credit_transaction in credit_transactions:
            if credit_transaction.amount != 0:
                paid = False
        credit.paid = paid
        credit.save()
        messages.success(self.request, "Плата по кредиту успешна произведена!")
        return HttpResponseRedirect('/bank-account/my-credit/')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PayCreditView(LoginConfirmedRequiredMixin, View):
    model = CreditTransaction
    form_class = PayCreditForm
    success_url = reverse_lazy('my-credit')
    template_name = 'credit/pay_credit.html'
    pk_url_kwarg = 'id'
    def form_valid(self, form):
        credit = UserCredit.objects.filter(id=self.kwargs['id']).first()
        amount = form.cleaned_data['amount']
        bank_account = BankAccount.objects.filter(name=form.cleaned_data['bank_account']).first()
        credit_transactions = CreditTransaction.objects.filter(credit=credit)
        if bank_account.balance < amount:
            messages.success(self.request, "На банковском счете недостаточно средств для оплаты!")
            credit_transactions.save()
            return super().form_valid(form)
        if bank_account.currency != credit.credit.currency:
            messages.success(self.request, "Не возможно оплатить кредит, разные валюты!")
            return super().form_valid(form)

        for credit_transaction in credit_transactions:
            if credit_transaction.amount > 0:
                if credit_transaction.amount > amount:
                    credit_transaction.amount -= amount
                    amount = 0
                else:
                    credit_transaction.amount = 0
                    amount -= credit_transaction.amount
            credit_transaction.save()
        paid = True
        for credit_transaction in credit_transactions:
            if credit_transaction.amount != 0:
                paid = False
        credit.paid = paid
        credit.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DepositHistoryView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        deposit_transactions = DepositTransaction.objects.filter(deposit__id=id)
        context = {
            'deposit_transactions': deposit_transactions,
        }
        return render(request, 'bank_account/deposit_transaction.html', context)


class PayDepositView(LoginConfirmedRequiredMixin, CreateView):
    model = UserDeposit
    form_class = PayDepositForm
    success_url = reverse_lazy('my-deposit')
    template_name = 'bank_account/make-bank-account.html'

    def form_valid(self, form):
        CreditTransaction.objects.filter(pk=self.kwargs['pk'])
        credit_transaction = self.get_object()
        # Получаем введенную сумму из формы
        amount = form.cleaned_data['amount']
        # Уменьшаем значение amount у выбранного CreditTransaction
        credit_transaction.amount -= amount
        credit_transaction.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

