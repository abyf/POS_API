from django import forms
from .models import Payment, CardHolder, Merchant,Manager
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .serializers import PaymentSerializer
from decimal import Decimal
from django.db.models import Q, F
from django.db import transaction
from django.core.mail import EmailMessage
from django.conf import settings

class PaymentForm(forms.ModelForm):
    card_info = forms.CharField(label='CARD_ID/QR_CODE', max_length=100, required=True,widget=forms.TextInput(attrs={'size':'30'}))

    class Meta:
        model = Payment
        fields = ('amount','card_info','wallet_id')

        widgets = {
                'amount': forms.NumberInput(attrs={'size':'30'}),
                'wallet_id': forms.HiddenInput(),
           }

    def clean_card_info(self):
        card_info = self.cleaned_data['card_info']
        try:
            cardholder = CardHolder.objects.get(Q(card_id=card_info)|Q(qr_code=card_info))
        except CardHolder.DoesNotExist:
            raise forms.ValidationError('Customer not found !!!')
        return cardholder

    @transaction.atomic    #Wrapping the transaction in an atomic block to ensure that all database operations are rolled back if an error occurs
    def charge_and_credit(self,merchant):
        serializer = PaymentSerializer(self.cleaned_data)
        amount = Decimal(serializer.data['amount'])
        cardholder = self.cleaned_data['card_info']
        if isinstance(cardholder,str):
            raise ValueError('Something ODD about the entered QR_code or card_id!!!')
        #Checking that the cardholder is a valid uuid
        if isinstance(cardholder,str) and uuid.UUID(cardholder,version=4):
            card_info = cardholder
            try:
                #Using the select_for_update method to lock the CarHolder record during the transaction to prevent concurrent access and updates to the same record.
                cardholder = CardHolder.objects.select_for_update().get(qr_code=card_info)
            except CardHolder.DoesNotExist:
                pass
        else:
            card_info = cardholder.card_id
            try:
                cardholder = CardHolder.objects.select_for_update().get(card_id=card_info)
            except CardHolder.DoesNotExist:
                raise ValueError('Customer not found!!!: Please enter a valied card ID or QR code')

        if amount <= 0 :
            raise ValueError('Invalid amount: Please enter the correct amount')
        if cardholder.balance < amount:
            raise ValueError('Insufficient funds, Please charge your card!!!')

       # Updating CardHolder and Merchant fields using F expressions to avoid race conditions
        commission = amount * Decimal('0.01')
        cardholder.balance = F('balance') - amount - commission
        cardholder.save()

        merchant.balance = F('balance') + amount
        merchant.save()

        try:
            manager = Manager.objects.get(username='zgame')
        except Manager.DoesNotExist:
            messages.error(request,'Manager not found',)
        manager.balance = F('balance') + commission
        manager.cardholder_commission = F('cardholder_commission') + commission
        manager.save()

        return cardholder

    def get_payload(self,cardholder,merchant):
        try:
            amount = Decimal(self.cleaned_data['amount'])
            commission = amount * Decimal('0.01')
            payload = {'card_id':cardholder.card_id,'qr_code':cardholder.qr_code,'amount':amount,'wallet_id':merchant.wallet_id,'commission_fee':commission}
            return payload
        except Exception as e:
            raise e

class MerchantAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self,user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'],code='inactive',)
        try:
            merchant = Merchant.objects.get(user=user)
        except Merchant.DoesNotExist:
            raise forms.ValidationError('Merchant Does not Exist! Please register an account at the nearest office counter',code='invalid_login',)
        if not merchant.is_active:
            raise forms.ValidationError(self.error_messages['inactive'],code='inactive')
        super().confirm_login_allowed(user)
