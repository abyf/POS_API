from django.urls import path
from . import views
from .views import PaymentView
from django.contrib.auth.views import LoginView

urlpatterns = [
        path('', views.PaymentView, name='payment'),
        path('payment/',views.PaymentView, name='payment'),
        path('login/',LoginView.as_view(), name='login'),
]
