from django.urls import path
from . import views
from .views import PaymentView, MyLoginView

urlpatterns = [
        path('', views.PaymentView, name='payment'),
        path('payment/',views.PaymentView, name='payment'),
        path('login/',views.MyLoginView.as_view(), name='login'),
]
