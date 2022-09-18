import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from getpaidpi import settings
from .managers import CustomUserManager
import string
import random
from django.utils.translation import gettext_lazy as _

all = string.ascii_uppercase + string.digits
merchant_id_generated = "".join(random.sample(all, 8))

from django.contrib.auth.models import UserManager


# class MyUser(AbstractUser):

#    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)

#    email = models.EmailField(_('email address'), unique = True)

#    native_name = models.CharField(max_length = 5)

#    phone_no = models.CharField(max_length = 10)

#    USERNAME_FIELD = 'email'

#    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

#    def __str__(self):

#        return "{}".format(self.email)

# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
# post_save.connect(create_profile, sender=User)
#
#
# def delete_user(sender, instance=None, **kwargs):
#     try:
#         instance.user
#     except User.DoesNotExist:
#         pass
#     else:
#         instance.user.delete()
# post_delete.connect(delete_user, sender=Profile)



# class MyUserManager(BaseUserManager):
#     def create_user(self, email, merchant_name, phone, business_type, merchant_address,
#         merchant_city, merchant_country, is_active, is_staff, is_superuser, date_joined,  password=None):
       
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             email=self.normalize_email(email),
#             merchant_name=merchant_name,
#             phone=phone,
#             business_type=business_type,
#             merchant_address=merchant_address,
#             merchant_city=merchant_city,
#             merchant_country=merchant_country,
#             is_active=True,
#             is_superuser=False,
#             is_staff=False,
#             date_joined=date_joined,
#             password=password,

#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, phone, password):
#         user = self.create_user(
#             email,
#             password=password,
#             phone=phone,
#         )
#         user.is_admin = True
#         user.is_superuser = True
#         user.is_staff = True
#         user.save(using=self._db)
#         return user



class MyUser(AbstractBaseUser):
    merchant_name = models.CharField(max_length=250, default="")
    phone = models.CharField(max_length=30, default="")
    email = models.EmailField( unique=True, default="")
#     # password = models.CharField(max_length=30)
#     # password_confirmation = models.CharField(max_length=30)
#     # password_validation = models.CharField(max_length=30)
#     business_type = models.CharField(max_length=255)
#     merchant_address = models.CharField(max_length=255)
#     merchant_city = models.CharField( max_length=128, default="Dubai")
#     merchant_country = models.CharField(max_length=50, default="UAE")
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     is_staff= models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)
#     # token = models.CharField(max_length=128, default="")

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def has_perm(self, perm, obj=None):
#         return self.is_superuser

#     def has_module_perms(self, app_label):
#         return self.is_superuser

#     def __str__(self):
#         return self.email

#
# class Profile(models.Model):
#     merchant_name = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default="")
#     # merchant_name = models.ForeignKey(User, on_delete=models.CASCADE)
#     bank_account = models.CharField(max_length=30)
#     bank_country = models.CharField(max_length=30, default="")
#     card_id = models.CharField(max_length=20, unique=True)
#     merchant_id = models.CharField(max_length=30, default="")
#     currency = models.CharField(max_length=3)
#     total_balance = models.DecimalField(max_digits=10, decimal_places=2)
#     available_balance = models.DecimalField(max_digits=10, decimal_places=2)
#     reserved_amount = models.DecimalField(max_digits=10, decimal_places=2)
#
#     def __str__(self):
#         return self.merchant_name


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
    # merchant_name = models.ForeignKey(Account, on_delete=models.CASCADE)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.transfer_type




