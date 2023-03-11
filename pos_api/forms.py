from django import forms
from .models import Payment

from smartcard.System import readers
from smartcard.util import toHexString

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount','card_id')

        
        widgets = {
                'amount': forms.NumberInput(attrs={'size':'30'}),
                'card_id': forms.TextInput(attrs={'size':'30'}),
                #'reader_id': forms.TextInput(attrs={'size':'30'})
           }
           
    def detect_card(self):
            r = readers()
            if len(r) == 0:
                    raise forms.ValidationError("No readers found")
            connection = r[0].createConnection()
            connection.connect()
            data,sw1,sw2 = connection.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])
            card_id = toHexString(data).replace(" ","")
            #reader_id = r[0].replace(" ","")
            self.fields['card_id'] = card_id
            #self.fields['reader_id'] = card_id
        
    """def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.r = readers()
        if not self.r:
                raise forms.ValidationError("No readers found")
        self.connection = self.r[0].createConnection()
        self.connection.connect()
        data,sw1,sw2 = self.connection.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])
        self.card_id = toHexString(data).replace(" ","")
        self.fields['card_id'].initial = self.card_id"""
        


