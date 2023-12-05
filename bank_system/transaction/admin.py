from django.contrib import admin

from transaction.models import TransactionType, TransactionStatus, Transaction

admin.site.register(Transaction)
admin.site.register(TransactionStatus)
admin.site.register(TransactionType)
