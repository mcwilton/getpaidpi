from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import status, views
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, )
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers, models
from .models import Profile, Order, Product, Transaction
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import ProfileSerializer, OrderSerializer, ProductSerializer, BalanceExposeSerializer,ProductExposeSerializer,PayExposeSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Pay_API(APIView):
    serializer_class = PayExposeSerializer
    type_param_config = openapi.Parameter(
        'type', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    merchant_id_param_config = openapi.Parameter(
        'merchant_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    transaction_id_param_config = openapi.Parameter(
        'transaction_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    merchant_name_param_config = openapi.Parameter(
        'merchant_name', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    merchant_mcc_param_config = openapi.Parameter(
        'merchant_mcc', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    billing_amount_param_config = openapi.Parameter(
        'billing_amount', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    billing_currency_param_config = openapi.Parameter(
        'billing_currency', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    transaction_amount_param_config = openapi.Parameter(
        'transaction_amount', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    transaction_currency_param_config = openapi.Parameter(
        'transaction_currency', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    settlement_amount_param_config = openapi.Parameter(
        'settlement_amount', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    settlement_currency_param_config = openapi.Parameter(
        'settlement_currency', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)


    @swagger_auto_schema(manual_parameters=[type_param_config, merchant_id_param_config, transaction_id_param_config, merchant_name_param_config,merchant_mcc_param_config, billing_amount_param_config, billing_currency_param_config, transaction_amount_param_config, transaction_currency_param_config, settlement_amount_param_config, settlement_currency_param_config   ])
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

        account = models.Profile.objects.get(merchant_id=data.get('merchant_id'))

        if not float(account.total_balance) >= float(data.get('billing_amount')):
            raise ValueError

        account.reserved_amount = float(data.get('billing_amount'))

        account.available_balance = float(account.total_balance) - float(account.reserved_amount)

        transaction = models.Transaction(
            transaction_id=data.get('transaction_id'),
            type='authorisation',
            merchant_id=account.merchant_id,
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

#
# class RegisterMerchant(APIView):
#     def ran(self, request):
#         serializer = serializers.UserSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             data = serializer.data
#             return data
#
#     def post(self, data):
#         register = models.Transaction(
#             merchant_name=data.get('merchant_name'),
#             email=data.get('email'),
#             merchant_city=data.get('merchant_city'),
#             merchant_country=data.get('merchant_country'),
#             phone=data.get('phone'),
#             merchant_address=data.get('merchant_address'),
#             transaction_currency=data.get('transaction_currency')
#         )
#
#         register.save()
#
#         return Response(
#             data={
#                 'error': False,
#                 'message': f'Payment successful for merchant :{data.get("merchant_name")}'
#             },
#             status=status.HTTP_201_CREATED
#         )


class Transactions_API(APIView):
    # @swagger_auto_schema(operation_summary="Create a user account by signing Up")
    def get(self, request):
        serializer = serializers.TransactionsSerializer(
            data=request.query_params)

        try:
            if serializer.is_valid(raise_exception=True):

                accounts = models.Profile.objects.get(merchant_id=serializer.data.get('merchant_id'))

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


class Balances_API(views.APIView):
    serializer_class = BalanceExposeSerializer
    merchant_id_param_config = openapi.Parameter(
        'merchant_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    type_param_config = openapi.Parameter(
        'type', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[merchant_id_param_config, type_param_config])
    def get(self, request):

        serializer = serializers.BalancesSerializer(data=request.query_params)

        try:
            if serializer.is_valid(raise_exception=True):
                # Fetch required accounts
                accounts = models.Profile.objects.filter(
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


class ProfileListCreateView(ListCreateAPIView):
    queryset= Profile.objects.all()
    serializer_class= ProfileSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)


class ProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset= Profile.objects.all()
    serializer_class= ProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]


class OrderView(APIView):
    # permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]
    # serializer_class = OrderExposeSerializer
    # merchant_id_param_config = openapi.Parameter(
    #     'merchant_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    # type_param_config = openapi.Parameter(
    #     'type', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    # @swagger_auto_schema(manual_parameters=[merchant_id_param_config, type_param_config])
    def get(self, request, format=None):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

class OrderDetail(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductView(APIView):
    # permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]
    serializer_class = ProductExposeSerializer
    product_id_param_config = openapi.Parameter(
        'product_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    product_name_param_config = openapi.Parameter(
        'product_name', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    merchant_name_param_config = openapi.Parameter(
        'merchant_name', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    product_price_param_config = openapi.Parameter(
        'product_price', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)


    @swagger_auto_schema(manual_parameters=[product_id_param_config, product_name_param_config, merchant_name_param_config, product_price_param_config ])
    def get(self, request, format=None):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(manual_parameters=[product_id_param_config, product_name_param_config, merchant_name_param_config, product_price_param_config ])
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



