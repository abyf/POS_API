from django.urls import path
from django.contrib import admin
from . import views
from .views import PaymentView, MyLoginView,homepage

urlpatterns = [
        path('', views.homepage, name='home'),
        path('admin/', admin.site.urls, name='admin'),
        path('', views.PaymentView, name='payment'),
        path('payment/',views.PaymentView, name='payment'),
        path('login/',views.MyLoginView.as_view(), name='login'),
]
