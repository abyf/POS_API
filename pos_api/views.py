from decimal import Decimal
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import CardHolderSerializer,MerchantSerializer,PaymentSerializer,TransactionSerializer
from .forms import PaymentForm
from django import forms
from django.forms import ValidationError
import requests
from .models import CardHolder, Merchant, Payment, Transaction

class PaymentView(APIView):
    """ API view to handle payment from the customer's card to the merchant account"""
    
    serializer_class = PaymentSerializer
    
    def get(self,request):
        form = PaymentForm(request.POST)
        return render(request,'payment.html',{'form': form})
    
    def post(self,request):
        # Validate the form data
        form = PaymentForm(request.POST)
        if not form.is_valid():
            error_msg= form.errors
            return render(request, 'payment.html',{'form': form,'error_msg': error_msg})
            
        #serialize the form data for consistency
        serializer = PaymentSerializer(form.cleaned_data)
            
        amount = Decimal(serializer.data['amount'])
        card_id = serializer.data['card_id']
        
        # Fetch the card_id associated to the account details
        cardholder = CardHolder.objects.get(card_id = card_id)
            
         # Double check that cardholder has enough funds   
        if cardholder.balance < amount:
            error_msg= 'Balance is Insufficient, please recharge your card!!!'
            return render(request, 'payment.html',{'form': form,'error_msg': error_msg})
            
        # Deduct the spent amount from the cardholder balance  and save it 
        cardholder.balance = cardholder.balance - amount
        cardholder.save()
        
        # Create and save the transaction
    
        #transaction = Transaction()

        #transaction.save()
        
        # Sent notification to the cardholder and the merchant
            
        # serialize the form data for consistency
        #serializer = PaymentSerializer(payment)
        
        return render(request, 'success.html',{'form': form})

