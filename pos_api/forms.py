from django import forms
from .models import Payment, CardHolder

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount','card_id')
        
        widgets = {
                'amount': forms.NumberInput(attrs={'size':'30'}),
                'card_id': forms.TextInput(attrs={'size':'30'})
           }

#        def clean_card_id(self):
#        card_id = self.cleaned_data['card_id']
#        try:
#            cardholder = CardHolder.objects.get(card_id=card_id)
#        except cardHolder.DoesNotExist:
#            raise forms.ValidationError('Invalid card ID')
#        return cardholder

#    def save (self,merchant):
#        payment = super().save(commit=False)
#        payment.reader_id = merchant
#        payment.card_id = self.cleaned_data['card_id']
#        payment.save()
#
#        cardholder = self.cleaned_data['card_id']
#        cardholder.balance -= payment.amount
#        cardholder.save()

#        merchant.balance += payment.amount
#        merchant.save()

#       return payment

