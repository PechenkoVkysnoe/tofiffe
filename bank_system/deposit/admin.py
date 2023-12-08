from django.contrib import admin

from deposit.models import Deposit, UserDeposit, DepositTransactionType, DepositTransaction

admin.site.register(Deposit)
admin.site.register(UserDeposit)
admin.site.register(DepositTransactionType)
admin.site.register(DepositTransaction)
