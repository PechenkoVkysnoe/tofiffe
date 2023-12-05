from django import forms
from bank_account.models import BankAccount, Currency, CreditCardType, CreditCard

from transaction.models import TransactionType, Transaction


class MoneyTransferForm(forms.ModelForm):
    credit_card_to = forms.CharField(max_length=16)

    class Meta:
        model = Transaction
        fields = ['value', 'credit_card_from']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['credit_card_from'].queryset = CreditCard.objects.filter(bank_account__user=user)

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value <= 0:
            raise forms.ValidationError("Value must be a positive number.")
        return value

    def clean_credit_card_to(self):
        credit_card_to = self.cleaned_data.get('credit_card_to')
        credit_card_to = CreditCard.objects.filter(number=credit_card_to).first()
        if credit_card_to is None:
            raise forms.ValidationError("Incorrect credit card to")
        return credit_card_to
