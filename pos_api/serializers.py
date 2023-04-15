from rest_framework import serializers
from .models import CardHolder,Merchant,Payment

class CardHolderSerializer(serializers.ModelSerializer):
	class Meta:
		model = CardHolder
		fields = ('card_id','qr_code','balance')


class MerchantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Merchant
		fields = ('wallet_id','balance')

class PaymentSerializer(serializers.ModelSerializer):
	card_info = serializers.UUIDField(required=True)

	class Meta:
		model = Payment
		fields = ('amount','card_info','wallet_id')

class WebhookSerializer(serializers.Serializer):
	card_id = serializers.CharField(max_length=120, required=False)
	qr_code = serializers.CharField(max_length=120,required=False)
	wallet_id = serializers.UUIDField()
	amount = serializers.DecimalField(max_digits=250, decimal_places=2)
	commission_fee = serializers.DecimalField(max_digits=250,decimal_places=2)

	def validate(self,attrs):
		if not attrs.get('card_id') and not attrs.get('qr_code'):
			raise serializers.ValidationError("Either 'card_id' or 'qr_code' is required.")
		if attrs.get('card_id') and attrs.get('qr_code'):
			raise serializers.ValidationError("Only one of 'card_id' or 'qr_code' is required.")

		return attrs
