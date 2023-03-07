from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount','card_id')
        
        widgets = {
                'amount': forms.NumberInput(attrs={'size':'30'}),
                'card_id': forms.TextInput(attrs={'size':'30'})
           }
