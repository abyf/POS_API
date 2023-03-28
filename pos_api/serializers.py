from rest_framework import serializers
from .models import CardHolder,Merchant,Payment,Transaction

class CardHolderSerializer(serializers.ModelSerializer):
	class Meta:
		model = CardHolder
		fields = ('card_id','qr_code','balance')


class MerchantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Merchant
		fields = ('wallet_id','balance')

class PaymentSerializer(serializers.ModelSerializer):
	#card_info = serializers.CharField(max_length=100,required=True)

	class Meta:
		model = Payment
		fields = ('card_id','qr_code','amount')

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = '__all__'
