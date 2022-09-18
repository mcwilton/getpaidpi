import random
import string
from datetime import timezone

from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db.models.signals import post_save, post_delete

all = string.ascii_uppercase + string.digits
merchant_id_generated = "".join(random.sample(all, 8))

from getpaidpi import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None,  **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username, email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email


class Profile(models.Model):
    GENDER = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, default="")
    business_name = models.CharField(max_length=250, default="")
    business_type = models.CharField(max_length=255)
    merchant_address = models.CharField(max_length=255)
    merchant_city = models.CharField(max_length=128, default="Dubai")
    merchant_country = models.CharField(max_length=50, default="UAE")
    bank_account = models.CharField(max_length=30)
    bank_country = models.CharField(max_length=30, default="")
    card_id = models.CharField(max_length=20, unique=True)
    merchant_id = models.CharField(max_length=30, default="")
    currency = models.CharField(max_length=3)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    available_balance = models.DecimalField(max_digits=10, decimal_places=2)
    reserved_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.business_name


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
    created = models.DateTimeField('created', auto_now_add=True)

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
    # merchant_name = models.ForeignKey(Account, on_delete=models.CASCADE)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField('created', auto_now_add=True)

    def __str__(self):
        return self.transfer_type




