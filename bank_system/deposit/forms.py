from django import forms
from bank_account.models import BankAccount, Currency, CreditCardType, CreditCard


from credit.models import UserCredit

from deposit.models import UserDeposit


class CreateDepositForm(forms.ModelForm):
    class Meta:
        model = UserDeposit
        fields = ['deposit', 'bank_account', 'amount']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = BankAccount.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        amount = self.cleaned_data.get('amount')
        deposit = self.cleaned_data.get('deposit')
        if amount is None:
            raise forms.ValidationError("Значение должно быть меньше разрешенного максимума")
        else:
            if amount > deposit.max_amount:
                raise forms.ValidationError("Значение должно быть меньше разрешенного максимума")
            if amount < deposit.min_amount:
                raise forms.ValidationError("Значение должно быть больше разрешенного минимума")
        return cleaned_data
