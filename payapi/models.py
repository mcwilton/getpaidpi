from enum import unique
from django.db import models
from django.utils import timezone


class Customer(models.Model):
    customer_name = models.CharField(max_length=30)
    bank_account = models.CharField(max_length=30)
    bank_country = models.CharField(max_length=100)
    credit_card_id = models.IntegerField()
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.customer_name


class Account(models.Model):

    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card_id = models.CharField(max_length=16)
    credit_card_id = models.CharField(max_length=20, unique=True)
    currency = models.CharField(max_length=3)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    available_balance = models.DecimalField(max_digits=10, decimal_places=2)
    reserved_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.card_id


class Transaction(models.Model):

    transaction_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=16)
    credit_card_id = models.OneToOneField(Customer, on_delete=models.CASCADE, unique=True)
    merchant_name = models.CharField(max_length=100)
    merchant_country = models.CharField(max_length=4)
    merchant_city = models.CharField(max_length=128, null=True, default=None)
    merchant_mcc = models.IntegerField()
    billing_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_currency = models.CharField(max_length=3)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_currency = models.CharField(max_length=3)
    settlement_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    settlement_currency = models.CharField(max_length=3, null=True, default=None)
    settled = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.transaction_id


class Transfer(models.Model):

    CREDIT = 'CRT'
    DEBIT = 'DBT'
    TRANSFER_TYPE_CHOICES = (
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    )

    transfer_type = models.CharField(max_length=3, choices=TRANSFER_TYPE_CHOICES, blank=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, to_field='transaction_id',
                                    null=True, default=None)  # Available if debit.
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.transfer_type




