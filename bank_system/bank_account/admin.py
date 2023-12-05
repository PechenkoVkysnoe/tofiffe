from django.contrib import admin
from bank_account.models import (
    Currency,
    CurrencyRelation,
    BankAccountType,
    BankAccount,
    CreditCardType,
    CreditCard,
    BankPartner,
    PrivilegeType,
    Privileges,
    CardTypePrivileges
)

admin.site.register(Currency)
admin.site.register(CurrencyRelation)
admin.site.register(BankAccountType)
admin.site.register(BankAccount)
admin.site.register(CreditCardType)
admin.site.register(CreditCard)
admin.site.register(BankPartner)
admin.site.register(PrivilegeType)
admin.site.register(Privileges)
admin.site.register(CardTypePrivileges)
