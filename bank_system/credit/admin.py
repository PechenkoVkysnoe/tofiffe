from django.contrib import admin

from credit.models import Credit, CreditStatus, UserCredit, CreditType, CreditTransaction

admin.site.register(Credit)
admin.site.register(CreditStatus)
admin.site.register(UserCredit)
admin.site.register(CreditType)
admin.site.register(CreditTransaction)