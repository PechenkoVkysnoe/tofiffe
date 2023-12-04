from django.contrib import admin
from bank_account.models import Currency, CurrencyRelation, BankAccountType, BankAccount, CreditCardType, CreditCard

admin.site.register(Currency)
admin.site.register(CurrencyRelation)
admin.site.register(BankAccountType)
admin.site.register(BankAccount)
admin.site.register(CreditCardType)
admin.site.register(CreditCard)
