from django import forms
from .models import Payment, CardHolder
from .serializers import PaymentSerializer
from decimal import Decimal

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount','card_id')

        widgets = {
                'amount': forms.NumberInput(attrs={'size':'30'}),
                'card_id': forms.TextInput(attrs={'size':'30'})
           }
        error_messages = {
           'card_id': {'invalid_choice': 'User does not exist!!!'}
           }

    def clean_card_id(self):
        serializer = PaymentSerializer(self.cleaned_data)
        card_id = serializer.data['card_id']
        try:
            cardholder = CardHolder.objects.get(card_id=card_id)
        except CardHolder.DoesNotExist:
            raise forms.ValidationError('User does not exist!!!')
        return cardholder

    def charge_and_credit(self,merchant):
        serializer = PaymentSerializer(self.cleaned_data)
        card_id = serializer.data['card_id']

        cardholder = CardHolder.objects.get(card_id=card_id)
        amount = Decimal(serializer.data['amount'])

        if amount <= 0 :
            raise ValueError('Invalid amount: Please enter the correct amount')
        if cardholder.balance < amount:
            raise ValueError('Insufficient funds, Please charge your card!!!')

        cardholder.balance -= amount
        cardholder.save()
        merchant.balance += amount
        merchant.save()

        payment = self.save(commit=False)
        payment.reader_id = merchant
        payment.save()
