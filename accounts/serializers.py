from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Product, Order

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password")


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


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class BalanceExposeSerializer(serializers.ModelSerializer):
    merchant_id = serializers.IntegerField()
    type = serializers.CharField(max_length=9)

    class Meta:
        model = User
        fields = ['merchant_id', 'type']


class ProductExposeSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(max_length=90)
    product_name = serializers.CharField(max_length=90)
    merchant_name = serializers.CharField(max_length=90)
    product_price = serializers.CharField(max_length=90)

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'merchant_name', 'product_price']


class PayExposeSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Product
        fields = ['type', 'merchant_id', 'transaction_id', 'merchant_mcc', 'billing_amount', 'billing_currency',
                  'transaction_amount', 'transaction_currency', 'settlement_amount', 'settlement_currency']
