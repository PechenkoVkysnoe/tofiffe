from django import forms
from bank_account.models import BankAccount, Currency, CreditCardType, CreditCard


from credit.models import UserCredit


class CreateCreditForm(forms.ModelForm):
    class Meta:
        model = UserCredit
        fields = ['credit', 'bank_account', 'amount']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = BankAccount.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        amount = self.cleaned_data.get('amount')
        credit = self.cleaned_data.get('credit')
        if amount is None:
            raise forms.ValidationError("Значение должно быть меньше разрешенного максимума")
        else:
            if amount > credit.max_amount:
                raise forms.ValidationError("Значение должно быть меньше разрешенного максимума")
            if amount < credit.min_amount:
                raise forms.ValidationError("Значение должно быть больше разрешенного минимума")
        return cleaned_data
