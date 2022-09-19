from django.contrib import admin

from . import models
from .models import Transfer

admin.site.register(Transfer)
# #

@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('username','first_name','last_name',
                    'email', 'is_active')
    list_filter = ('is_active',
                   'username')
    list_per_page = 10

    search_fields = ('username', 'is_active')

# #
@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ('merchant_id',
                    'currency', 'total_balance', 'merchant_country')
    list_filter = ( 'merchant_id',
                    'currency')
    list_per_page = 10
    search_fields = ( 'merchant_id',)
#
@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = ('transaction_id', 'merchant_name',
                    'billing_currency', 'billing_amount', 'settled')
    list_filter = ('transaction_id', 'merchant_name',
                    'billing_currency', 'settled', 'merchant_id')
    list_per_page = 10

    search_fields = ('transaction_id', 'merchant_name', 'settled', 'merchant_id')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('product_id', 'merchant_name',
                    'product_name', 'product_price')

    list_filter = ('product_id', 'merchant_name'
                   )
    list_per_page = 10

    search_fields = ('product_id', 'merchant_name', 'product_name')


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ('order_id', 'merchant_name', 'product_name',
                    'number_of_products', 'customer_name', 'customer_address')

    list_filter = ('order_id', 'merchant_name', 'product_name')
    list_per_page = 10

    search_fields = ('order_id', 'merchant_name')