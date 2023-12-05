from django.db import models
from bank_account.models import BankAccount

COUNT = 0


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

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        global COUNT

        if self.status.name == 'Одобрено' and not COUNT:
            COUNT += 1
            self.bank_account.balance += self.amount
            self.bank_account.save()
        super().save(*args, **kwargs)


class CreditTransaction(models.Model):
    dt = models.DateTimeField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    credit = models.ForeignKey(UserCredit, on_delete=models.CASCADE)

    class Meta:
        ordering = ['dt']

