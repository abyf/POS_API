from django.urls import path
from . views import UserLoginView,MerchantLoginView

urlpatterns = [
        path('login/',UserLoginView.as_view(), name='login'),
        path('merchantlogin/',MerchantLoginView.as_view(), name='merchantlogin'),
]
