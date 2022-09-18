
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, re_path, include
# from payapi import views
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="PayAPI",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    re_path(r'^api/v1/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("admin/", admin.site.urls),
    path("api/v1/", include("accounts.urls")),
    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.jwt")),

    # path('pay/', views.Pay_API.as_view()),
    # path('transactions/', views.Transactions_API.as_view()),
    # path('balances/', views.Balances_API.as_view()),
    # path('reg/', views.RegisterMerchant.as_view()),
    # path("t/", include("payapi.urls")),


]

# urlpatterns = format_suffix_patterns(urlpatterns)