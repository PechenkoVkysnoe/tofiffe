from django.contrib import admin

from transaction.models import TransactionType, TransactionStatus, CardTransaction, BankAccountTransaction

admin.site.register(CardTransaction)
admin.site.register(BankAccountTransaction)
admin.site.register(TransactionStatus)
admin.site.register(TransactionType)
