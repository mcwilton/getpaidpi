import random
import string
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.db import models
from getpaidpi import settings

all_digits = string.digits  # string.ascii_uppercase +
merchant_id_generated = "".join(random.sample(all_digits, 8))


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
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
    username = models.CharField(max_length=255, default='')
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=30, default="")
    business_name = models.CharField(max_length=250, default="")
    business_type = models.CharField(max_length=255)
    merchant_address = models.CharField(max_length=255)
    merchant_city = models.CharField(max_length=128, default="Dubai")
    merchant_country = models.CharField(max_length=50, default="UAE")
    bank_account = models.CharField(max_length=30)
    bank_country = models.CharField(max_length=30, default="")
    card_id = models.CharField(max_length=20, unique=True)
    merchant_id = models.DecimalField(max_digits=10, decimal_places=0, default=merchant_id_generated)
    currency = models.CharField(max_length=3)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    reserved_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.business_name


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=16)
    merchant_id = models.CharField(max_length=20, unique=True)
    merchant_name = models.CharField(max_length=100)
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


class Product(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    merchant_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    order_id = models.PositiveIntegerField()
    merchant_id = models.CharField(max_length=255)
    merchant_name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255, default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_products = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    customer_address = models.CharField(max_length=255)

    def __str__(self):
        return self.customer_name
