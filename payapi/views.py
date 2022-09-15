from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, permissions
from . import serializers, models
from .models import User, Profile, Transaction, Transfer
from .serializers import PaySerializer, TransactionsSerializer, BalancesSerializer
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


class Pay_API(APIView):

    def post(self, request):
        serializer = serializers.PaySerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            if serializer.data.get('type') == 'authorisation':
                response = self.authorisation(serializer.data)

            else:
                response = self.presentment(serializer.data)

        else:
            # print(serializer.errors)
            raise KeyError

        return response


    def authorisation(self, data):

        account = models.Account.objects.get(merchant_id=data.get('merchant_id'))

        if not float(account.total_balance) >= float(data.get('billing_amount')):
            raise ValueError

        account.reserved_amount = float(data.get('billing_amount'))

        account.available_balance = float(account.total_balance) - float(account.reserved_amount)

        transaction = models.Transaction(
            transaction_id=data.get('transaction_id'),
            type='authorisation',
            merchant_id=account,
            billing_amount=data.get('billing_amount'),
            billing_currency=data.get('billing_currency'),
            merchant_name=data.get('merchant_name'),
            # merchant_country=data.get('merchant_country'),
            # merchant_mcc=data.get('merchant_mcc'),
            transaction_amount=data.get('transaction_amount'),
            transaction_currency=data.get('transaction_currency')
        )

        account.save()
        transaction.save()

        return Response(
            data={
                'error': False,
                'message': f'Payment successful for merchant_id:{data.get("merchant_id")} with transaction id:{data.get("transaction_id")}'
            },
            status=status.HTTP_200_OK
        )


class Transactions_API(APIView):

    def get(self, request):
        serializer = serializers.TransactionsSerializer(
            data=request.query_params)

        try:
            if serializer.is_valid(raise_exception=True):

                accounts = models.Account.objects.get(merchant_id=serializer.data.get('merchant_id'))

                start_date = serializer.data.get('start_date')
                end_date = serializer.data.get('end_date')

                transactions = models.Transaction.objects.filter(
                    type='authorisation',
                    merchant_id=accounts,
                    # date__range=(start_date, end_date)
                )

                if transactions:
                    transactions_data = {}

                    for i in transactions:
                        if i.merchant_id not in transactions_data:
                            transactions_data[i.merchant_id] = []

                        transactions_data[i.merchant_id].append({
                            'transaction_id': i.transaction_id,
                            'merchant_name': i.merchant_name,
                            'billing_amount': i.billing_amount,
                            'billing_currency': i.billing_currency,
                            'date': i.timestamp
                        })

                    response = Response(
                        data={
                            'error': False,
                            'message': f'Transactions for Merchant: {serializer.data.get("merchant_id")}',
                            'data': transactions_data
                        },
                        status=status.HTTP_200_OK
                    )

                else:
                    response = Response(
                        data={
                            'error': True,
                            'message': f'No transactions for Merchant: {serializer.data.get("merchant_id")}'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )

            else:
                raise KeyError

        except ObjectDoesNotExist:
            response = Response(
                data={
                    'error': True,
                    'message': f'No transactions for Merchant: {serializer.data.get("merchant_id")}'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except KeyError:
            response = Response(
                data={
                    'error': True,
                    'message': 'BAD REQUEST',
                    'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return response


class Balances_API(APIView):

    def get(self, request):

        serializer = serializers.BalancesSerializer(data=request.query_params)

        try:
            if serializer.is_valid(raise_exception=True):
                # Fetch required accounts
                accounts = models.Account.objects.filter(
                    merchant_id=serializer.data.get('merchant_id'))

                transactions_data = {}

                if serializer.data.get('type') == 'ledger':
                    transactions = models.Transaction.objects.filter(
                        type='presentment',
                        merchant_id=accounts
                    )

                    if transactions:
                        for i in transactions:
                            if i.merchant_id.merchant_id not in transactions_data:
                                transactions_data[i.merchant_id.merchant_id] = {
                                    'authorisation': 0,
                                    'presentment': 0
                                }

                            transactions_data[i.merchant_id.merchant_id][i.type] += float(
                                i.billing_amount)

                accounts_data = {}

                for i in accounts:
                    if i.merchant_id not in accounts_data:
                        accounts_data[i.merchant_id] = {
                            'balance': float(i.total_balance),
                            'currency': i.currency
                        }

                    if transactions_data and \
                            (i.merchant_id in transactions_data) and \
                            (serializer.data.get('type') == 'ledger'):

                        accounts_data[i.merchant_id]['balance'] += transactions_data[i.merchant_id]['authorisation']

                response = Response(
                    data={
                        'error': False,
                        'message': f'Balances found for Merchant {serializer.data.get("merchant_id")}',
                        'data': accounts_data
                    },
                    status=status.HTTP_200_OK
                )

            else:
                raise KeyError

        except ObjectDoesNotExist:
            response = Response(
                data={
                    'error': True,
                    'message': f'No account found for Merchant <{serializer.data.get("merchant_id")}>'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except KeyError:
            response = Response(
                data={
                    'error': True,
                    'message': 'Bad request data',
                    'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return response
