# from django.contrib import admin
#
# from . import models
# from .models import MyUser, Profile, Transaction, Transfer
#
# # admin.site.register(Merchant)
# # admin.site.register(Account)
# # admin.site.register(Transaction)
# admin.site.register(Transfer)
# #
# #
# # @admin.register(models.MyUser)
# # class MyUserAdmin(admin.ModelAdmin):
# #
# #     list_display = ('merchant_name',
# #                     'email', )#'is_active')
# #     # list_editable = ('customer_name',)
# #     list_filter = ('merchant_name',
# #                    )#'is_active')
# #     list_per_page = 10
# #
# #     search_fields = ('merchant_name', )#'is_active')
#
# #
# # @admin.register(models.Profile)
# # class ProfileAdmin(admin.ModelAdmin):
# #
# #     list_display = ('merchant_id',
# #                     'currency', 'total_balance')
# #     # list_editable = ('customer_name',)
# #     list_filter = ( 'merchant_id',
# #                     'currency')
# #     list_per_page = 10
# #
# #     search_fields = ( 'merchant_id',)
#
# @admin.register(models.Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#
#     list_display = ('transaction_id', 'merchant_name',
#                     'billing_currency', 'billing_amount', 'settled', 'timestamp')
#     # list_editable = ('customer_name',)
#     list_filter = ('transaction_id', 'merchant_name',
#                     'billing_currency', 'settled', 'merchant_id')
#     list_per_page = 10
#
#     search_fields = ('transaction_id', 'merchant_name', 'settled', 'merchant_id')