from django.urls import path
from . import views
from .views import PaymentView
urlpatterns = [
        path('payment/',views.PaymentView, name='payment'),
]
