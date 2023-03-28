from django.db import models
import uuid
from django.contrib.auth.models import User, Group


class CardHolder(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=120, null=True, blank=True)
    card_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    qr_code = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{name}:{card_id}".format(name=self.name,card_id=self.card_id)

class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,default=2)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=250,null=True, blank=True)
    email = models.EmailField(max_length=120,null=True, blank=True)
    reader_id = models.CharField(max_length=50,null=True, blank=True, unique=True)
    wallet_id = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    balance = models.DecimalField(max_digits=250,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{name}:{phone}".format(name=self.name,phone=self.phone)

    def save(self,*args,**kwargs):
        if not self.pk:
            #If this is a new Merchant, add them to the merchant Group
            group = Group.objects.get(name='merchant')
            self.user.groups.add(group)
        super().save(*args, **kwargs)


class Payment(models.Model):
    card_id = models.CharField(max_length=120, blank=True)
    qr_code = models.ForeignKey(CardHolder, on_delete=models.CASCADE, null=True, blank=True)
    wallet_id = models.ForeignKey(Merchant,on_delete=models.CASCADE,to_field='wallet_id')
    amount = models.DecimalField(max_digits=250,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_cardholder(self):
        try:
            return CardHolder.objects.get(card_id=self.card_id)
        except CardHolder.DoesNotExist:
            return CardHolder.objects.get(qr_code=self.qr_code)

    def __str__(self):
        cardholder = self.get_cardholder()
        return f"{self.amount} was paid to {self.wallet_id.name} by {self.CardHolder.name}"

class Transaction(models.Model):
    cardholder_id = models.CharField(max_length=50, blank=True)
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
