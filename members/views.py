from django.shortcuts import render
# from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from members.forms import MerchantAuthenticationForm
from django.urls import reverse_lazy

class UserLoginView(LoginView):
	form_class = AuthenticationForm
	template_name = 'registration/login.html'
	#success_url = reverse_lazy('payment') 

class MerchantLoginView(LoginView):
	form_class = MerchantAuthenticationForm
	template_name = 'registration/merchantlogin.html'
	#success_url = reverse_lazy('payment') 
