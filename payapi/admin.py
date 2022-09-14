from django.contrib import admin

from . import models
from .models import Merchant, Account, Transaction, Transfer

# admin.site.register(Merchant)
# admin.site.register(Account)
# admin.site.register(Transaction)
admin.site.register(Transfer)


@admin.register(models.Merchant)
class MerchantAdmin(admin.ModelAdmin):

    list_display = ('merchant_name', 'merchant_id',
                    'email', 'is_active')
    # list_editable = ('customer_name',)
    list_filter = ('merchant_name', 'merchant_id',
                    'is_active')
    list_per_page = 10

    search_fields = ('merchant_name', 'merchant_id', 'is_active')


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):

    list_display = ('merchant_name', 'merchant_id',
                    'currency', 'total_balance')
    # list_editable = ('customer_name',)
    list_filter = ('merchant_name', 'merchant_id',
                    'currency')
    list_per_page = 10

    search_fields = ('merchant_name', 'merchant_id')

@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = ('transaction_id', 'merchant_name',
                    'billing_currency', 'billing_amount', 'settled', 'timestamp')
    # list_editable = ('customer_name',)
    list_filter = ('transaction_id', 'merchant_name',
                    'billing_currency', 'settled', 'merchant_id')
    list_per_page = 10

    search_fields = ('transaction_id', 'merchant_name', 'settled', 'merchant_id')