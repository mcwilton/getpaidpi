from django.test import TestCase
from .models import Customer, Account, Transaction, Transfer
from django.test import RequestFactory
from django.urls import reverse
from model_mommy import mommy
from django.test import Client
from .views import Scheme_API


class TestCustomers(TestCase):
    def setUp(self):
        self.models = mommy.make('payapi.Customers')

    def test_str(self):
        self.assertEquals(str(self.models), self.models.customer_name)


class TestAccounts(TestCase):
    def setUp(self):
        self.models = mommy.make('payapi.Accounts')

    def test_str(self):
        self.assertEquals(str(self.models), self.models.credit_card_id)


class TestTransactions(TestCase):
    def setUp(self):
        self.models = mommy.make('payapi.Transactions')


class TestSchemeAPIView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.payapi_model = mommy.make('payapi.Accounts')
        self.customers_models = mommy.make('payapi.Customers', account=self.payapi_model, _quantity=3)


class TestSchemeAPIIntegration(TestCase):
    def setUp(self):
        self.client = Client()
        self.payapi_model = mommy.make('payapi.Accounts')
        self.customers_models = mommy.make('payapi.Customers', account=self.payapi_model, _quantity=3)



