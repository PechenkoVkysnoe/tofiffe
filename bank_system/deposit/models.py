from django.db import models
from bank_account.models import BankAccount
from bank_account.models import Currency


class Deposit(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    percent = models.IntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserDeposit(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.id)


class DepositTransactionType(models.Model):
    type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.type


class DepositTransaction(models.Model):
    dt = models.DateTimeField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    deposit = models.ForeignKey(UserDeposit, on_delete=models.CASCADE)
    type = models.ForeignKey(DepositTransactionType, on_delete=models.CASCADE)

    class Meta:
        ordering = ['dt']

