from rest_framework import serializers
from .models import CardHolder,Merchant,Payment,Transaction

class CardHolderSerializer(serializers.ModelSerializer):
	class Meta:
		model = CardHolder
		fields = ('card_id','balance')
	
	
class MerchantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Merchant
		fields = ('reader_id','balance')
	
class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = ('card_id','amount')

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = '__all__'

