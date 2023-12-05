import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, View, UpdateView

from bank_account.models import CreditCard, CurrencyRelation
from transaction.models import Transaction, TransactionStatus, TransactionType

from transaction.forms import MoneyTransferForm


class MoneyTransferView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = MoneyTransferForm
    template_name = 'transaction/money_transfer.html'
    success_url = reverse_lazy('my-transaction')
    # Мне стыдно за этот код....

    def form_valid(self, form):
        credit_card_from = form.cleaned_data['credit_card_from']
        credit_card_to = CreditCard.objects.filter(number=form.cleaned_data['credit_card_to']).first()

        if credit_card_from.bank_account.currency == credit_card_to.bank_account.currency:
            # если одинаковые валюты
            coef = 1
        else:
            # пытаюсь найти обмен
            currency_relation_direct = CurrencyRelation.objects.filter(
                currency_from=credit_card_from.bank_account.currency,
                currency_to=credit_card_to.bank_account.currency
            ).first()

            currency_relation_invert = CurrencyRelation.objects.filter(
                currency_from=credit_card_to.bank_account.currency,
                currency_to=credit_card_from.bank_account.currency
            ).first()
            currency_relation = currency_relation_direct or currency_relation_invert

            if currency_relation is None:
                # если такого обмена нет
                transaction_status = TransactionStatus.objects.get(type='нельзя конвертировать валюты')
            else:
                if currency_relation == currency_relation_direct:
                    coef = currency_relation.coefficient_buy
                else:
                    coef = currency_relation.coefficient_sell

        if credit_card_from.bank_account.balance / coef < form.cleaned_data['value']:
            transaction_status = TransactionStatus.objects.get(type='недостаточно средств')
        else:
            transaction_status = TransactionStatus.objects.get(type='успешно')

            # Update the balances of the credit cards
            credit_card_from.bank_account.balance -= form.cleaned_data['value'] * coef

            credit_card_from.bank_account.save()

            # без этого при переводе самому себе - изи деньги
            credit_card_to = CreditCard.objects.filter(number=form.cleaned_data['credit_card_to']).first()
            credit_card_to.bank_account.balance += form.cleaned_data['value']
            credit_card_to.bank_account.save()

        form.instance.dt = datetime.datetime.now()
        form.instance.transaction_type = TransactionType.objects.get(type='перевод')
        form.instance.value = form.cleaned_data['value']
        form.instance.credit_card_from = form.cleaned_data['credit_card_from']
        form.instance.credit_card_to = credit_card_to
        form.instance.transaction_status = transaction_status

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
