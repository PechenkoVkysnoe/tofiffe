from django.db import models
from bank_account.models import BankAccount

from bank_account.models import Currency

COUNT = {}

class CreditType(models.Model):
    type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.type


class Credit(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    period_in_month = models.IntegerField()
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    percent = models.IntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    type = models.ForeignKey(CreditType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CreditStatus(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserCredit(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    status = models.ForeignKey(CreditStatus, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        try:
            if self.status.name == 'Одобрено' and self.id not in COUNT:
                COUNT[self.id] = 1
                self.bank_account.balance += self.amount
                self.bank_account.save()
            super().save(*args, **kwargs)
        except:
            pass


class CreditTransaction(models.Model):
    dt = models.DateTimeField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    credit = models.ForeignKey(UserCredit, on_delete=models.CASCADE)

    class Meta:
        ordering = ['dt']

