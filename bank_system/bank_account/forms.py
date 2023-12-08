from django import forms
from bank_account.models import BankAccount, Currency, CreditCardType, CreditCard

from bank_account.models import BankAccountType

from credit.models import CreditTransaction

from deposit.models import UserDeposit

from deposit.models import DepositTransaction


class MakeBankAccountForm(forms.ModelForm):
    currency = forms.ModelChoiceField(queryset=Currency.objects.all())
    account_type = forms.ModelChoiceField(queryset=BankAccountType.objects.all())

    class Meta:
        model = BankAccount
        fields = ['currency']


class MakeCreditCardForm(forms.ModelForm):
    card_type = forms.ModelChoiceField(queryset=CreditCardType.objects.all())

    class Meta:
        model = CreditCard
        fields = ['owner_name', 'card_type', 'bank_account']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = BankAccount.objects.filter(user=user)


class PayCreditForm(forms.ModelForm):
    bank_account = forms.ModelChoiceField(queryset=BankAccount.objects.none())
    amount = forms.DecimalField(initial=0)
    class Meta:
        model = CreditTransaction
        fields = ['amount', 'bank_account']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = BankAccount.objects.filter(user=user)


class PayDepositForm(forms.ModelForm):
    bank_account = forms.ModelChoiceField(queryset=BankAccount.objects.none())
    amount = forms.DecimalField(initial=0)
    class Meta:
        model = DepositTransaction
        fields = ['amount', 'bank_account']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = BankAccount.objects.filter(user=user)
