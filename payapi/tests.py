from django.test import TestCase
from .models import  Transaction, Transfer #Customer, Account,
from django.test import RequestFactory
from django.urls import reverse
from model_mommy import mommy
from django.test import Client
# from .views import Scheme_API


class TestCustomers(TestCase):
    def setUp(self):
        self.models = mommy.make('payapi.Customer')

    def test_str(self):
        self.assertEquals(str(self.models), self.models.customer_name)


# class TestAccounts(TestCase):
#     def setUp(self):
#         self.models = mommy.make('payapi.Account')
#
#     def test_str(self):
#         self.assertEquals(str(self.models), self.models.credit_card_id)


class TestTransactions(TestCase):
    def setUp(self):
        self.models = mommy.make('payapi.Transaction')
#
#
# class TestSchemeAPIView(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.payapi_model = mommy.make('payapi.Account')
#         self.customers_models = mommy.make('payapi.Customer', account=self.payapi_model, _quantity=3)
#
#
# class TestSchemeAPIIntegration(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.payapi_model = mommy.make('payapi.Account')
#         self.customers_models = mommy.make('payapi.Customer', account=self.payapi_model, _quantity=3)



