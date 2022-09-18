from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import CustomUserManager
import string
import random
from django.utils.translation import gettext_lazy as _


all = string.ascii_uppercase + string.digits
merchant_id_generated = "".join(random.sample(all, 8))


class User(AbstractUser):
    merchant_name = models.CharField(max_length=30)
    email = models.EmailField(_('email address'), unique=True)
    merchant_city = models.CharField(max_length=128, default="Dubai")
    merchant_country = models.CharField(max_length=50, default="UAE")
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
# 	if created:
# 		Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
# 		instance.profile.save()

class Profile(models.Model):
    # merchant_name = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # merchant_name = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_account = models.CharField(max_length=30)
    bank_country = models.CharField(max_length=30, default="")
    card_id = models.CharField(max_length=20, unique=True)
    merchant_id = models.CharField(max_length=32, default=f"GPM-{merchant_id_generated}-2022")
    currency = models.CharField(max_length=3)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    available_balance = models.DecimalField(max_digits=10, decimal_places=2)
    reserved_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.merchant_name


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=16)
    merchant_id = models.CharField(max_length=20, unique=True)
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
    merchant_name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.transfer_type




