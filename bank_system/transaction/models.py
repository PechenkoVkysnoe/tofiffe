from django.db import models

from bank_account.models import CreditCard, BankAccount


class TransactionType(models.Model):
    type = models.CharField(primary_key=True, max_length=255)
    description = models.TextField(max_length=255)

    def __str__(self):
        return self.type


class TransactionStatus(models.Model):
    type = models.CharField(primary_key=True, max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.type


class CardTransaction(models.Model):
    dt = models.DateTimeField()
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_card_from = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='card_from')
    credit_card_to = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='card_to')
    transaction_status = models.ForeignKey(TransactionStatus, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-dt']


class BankAccountTransaction(models.Model):
    dt = models.DateTimeField()
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bank_account_from = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='bank_account_from')
    bank_account_to = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='bank_account_to')
    transaction_status = models.ForeignKey(TransactionStatus, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-dt']