from django.db import models
from django.utils import timezone
from members.models import User
from django.conf import settings


class CardHolder(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, unique=True)
    card_id = models.CharField(max_length=50,unique=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{name}:{card_id}".format(name=self.name,card_id=self.card_id)

class Merchant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, unique=True)
    reader_id = models.CharField(max_length=15,unique=True)
    balance = models.DecimalField(max_digits=250,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "{name}:{phone}".format(name=self.name,phone=self.phone)
        

class Payment(models.Model):
    card_id = models.ForeignKey(CardHolder,on_delete=models.CASCADE,to_field='card_id')
    reader_id = models.ForeignKey(Merchant,on_delete=models.CASCADE,to_field='reader_id')
    amount = models.DecimalField(max_digits=250,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '{amount}: {paid_to}'.format(amount =self.amount,paid_to=self.merchant_id)

class Transaction(models.Model):
    cardholder_id = models.ForeignKey(CardHolder,on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=250,decimal_places=2,null=True, blank=True)
    merchant_id = models.ForeignKey(Merchant,on_delete=models.SET_NULL, null=True,blank=True)
    transaction_fee = models.DecimalField(max_digits=250,decimal_places=2,null=True, blank=True)
    updated_amount = models.DecimalField(max_digits=250,decimal_places=2,null=True, blank=True)
    reference_id = models.CharField(max_length=200, blank=True)
    message = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{from_}: {to}'.format(from_=self.cardholder_id,to=self.merchant_id)



    
