from rest_framework import serializers
from .models import MyUser
# Profile, Transaction, Transfer
from django.db import transaction
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

   class Meta:

       model = MyUser

       fields = "__all__"

#
# class UserSerializer(serializers.Serializer):
#     type = serializers.CharField(max_length=16)
#     merchant_name = serializers.CharField(max_length=200)
#     email = serializers.CharField(max_length=100)
#     merchant_city = serializers.CharField(max_length=200)
#     merchant_country = serializers.CharField(max_length=200)
#     phone = serializers.CharField(max_length=30)
#     merchant_address = serializers.CharField(max_length=255)
#     password1 = serializers.CharField(max_length=128)
#     password2 = serializers.CharField(max_length=128)

    # @transaction.atomic
    # def save(self, request):
    #     user = super().save(request)
    #     user.merchant_name = self.data.get('merchant_name')
    #     user.email = self.data.get('email')
    #     user.merchant_city = self.data.get('merchant_city')
    #     user.merchant_country = self.data.get('merchant_country')
    #     user.save()
    #     return user


class PaySerializer(serializers.Serializer):

    type = serializers.CharField(max_length=16)
    merchant_id = serializers.IntegerField()
    transaction_id = serializers.CharField(max_length=16)
    merchant_name = serializers.CharField(max_length=255)
    merchant_mcc = serializers.IntegerField()
    billing_amount = serializers.DecimalField(max_digits=11, decimal_places=2)
    billing_currency = serializers.CharField(max_length=3)
    transaction_amount = serializers.DecimalField(max_digits=11, decimal_places=2)
    transaction_currency = serializers.CharField(max_length=3)
    settlement_amount = serializers.DecimalField(max_digits=11, decimal_places=2, required=False)
    settlement_currency = serializers.CharField(max_length=3, required=False)


class TransactionsSerializer(serializers.Serializer):

    merchant_id = serializers.IntegerField()
    # start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    # end_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')


class BalancesSerializer(serializers.Serializer):

    merchant_id = serializers.IntegerField()
    type = serializers.CharField(max_length=9)
