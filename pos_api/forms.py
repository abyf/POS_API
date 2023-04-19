from django import forms
from django.core.exceptions import ValidationError
from .models import Payment, CardHolder, Merchant,Manager
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,UserChangeForm
from .serializers import PaymentSerializer
from decimal import Decimal
from django.db.models import Q, F
from django.db import transaction
from django.contrib.auth.models import User
from django.conf import settings
import uuid

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)

        #widgets = {'is_superuser':forms.HiddenInput()}
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username',)


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

        if not card_info:
            raise forms.ValidationError('CARD_ID/QR_CODE filled should not be empty!!')

        try:
            card_info_uuid = uuid.UUID(card_info,version=4)
        except ValueError:
            raise forms.ValidationError('Invalid QR code or Card ID')

        try:
            cardholder = CardHolder.objects.get(Q(card_id=card_info_uuid)|Q(qr_code=card_info_uuid))
            if not cardholder.is_active:
                raise forms.ValidationError('Inactive cardholder!!! please activate this card at the nearest workstation')
        except CardHolder.DoesNotExist:
            raise forms.ValidationError('cardholder does not exist!!!')
        if cardholder.card_id == card_info_uuid:
            return str(cardholder.card_id)
        elif cardholder.qr_code == card_info_uuid:
            return str(cardholder.qr_code)
        else:
            raise forms.ValidationError('Unrecognized card ID or QR code')

    @transaction.atomic    #Wrapping the transaction in an atomic block to ensure that all database operations are rolled back if an error occurs
    def charge_and_credit(self,merchant):
        serializer = PaymentSerializer(self.cleaned_data)
        amount = Decimal(serializer.data['amount'])

        try:
            cardholder_id = self.clean_card_info()
            cardholder_id = uuid.UUID(cardholder_id,version=4)
        except forms.ValidationError as e:
            raise ValueError(str(e))

        try:
            #Using the select_for_update method to lock the CarHolder record during the transaction to prevent concurrent access and updates to the same record.
            cardholder = CardHolder.objects.select_for_update().get(Q(qr_code=cardholder_id)|Q(card_id=cardholder_id))
        except CardHolder.DoesNotExist:
            raise ValueError('cardholder does not exist!!!')

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

        payment = self.save(commit=False)
        payment.commission_fee = commission
        if cardholder.card_id == cardholder_id:
            payment.card_id = cardholder.card_id
        else:
            payment.qr_code = cardholder.qr_code
        payment.save()

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
