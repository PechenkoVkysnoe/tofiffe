from django.db import models

from bank_account.models import CreditCard


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


class Transaction(models.Model):
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