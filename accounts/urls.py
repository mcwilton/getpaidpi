from django.urls import path
from . import views

urlpatterns = [

    path('pay/', views.Pay_API.as_view()),
    path('transactions/', views.Transactions_API.as_view()),
    path('balances/', views.Balances_API.as_view()),

    path("profiles", views.ProfileListCreateView.as_view(), name="all-profiles"),
    path("profiles/<int:pk>", views.ProfileDetailView.as_view(), name="profile"),

    path("products", views.ProductView.as_view(), name="all-orders"),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name="order"),

    path("orders", views.OrderView.as_view(), name="all-products"),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name="product"),

]