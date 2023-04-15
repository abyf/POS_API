from django.db import models
import uuid,random,string
from django.contrib.auth.models import User, Group

class Manager(models.Model):
    username = models.CharField(max_length=120, unique=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    email = models.EmailField(max_length=120,null=True, blank=True)
    cardholder_commission = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    merchant_commission = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{username}:{balance}".format(username=self.username,balance=self.balance)

class CardHolder(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    address = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=120, null=True, blank=True)
    card_id = models.UUIDField(default=uuid.uuid4,editable=False, unique=True,null=True, blank=True)
    qr_code = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    alias = models.CharField(max_length=8,unique=True,editable=False)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE,default=3)

    def __str__(self):
        return "{name}:{phone}".format(name=self.name,phone=self.phone)

    def save(self,*args,**kwargs):
        if not self.pk:
            #If this is a new Administrator, add them to the Administrator Group
            group = Group.objects.get(name='cardholders')
            self.group = group
        if not self.alias:
            while True:
                new_alias = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                if not CardHolder.objects.filter(alias=new_alias).exists():
                    break
            self.alias = new_alias
        super().save(*args, **kwargs)

class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='merchants')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,default=2)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    address = models.CharField(max_length=250,null=True, blank=True)
    email = models.EmailField(max_length=120,null=True, blank=True)
    reader_id = models.CharField(max_length=50,null=True, blank=True, unique=True)
    wallet_id = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    alias = models.CharField(max_length=8,unique=True,editable=False)
    balance = models.DecimalField(max_digits=250,decimal_places=2,default=0,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{name}:{phone}".format(name=self.name,phone=self.phone)

    def save(self,*args,**kwargs):
        if not self.pk:
            #If this is a new Merchant, add them to the merchant Group
            group = Group.objects.get(name='merchant')
            self.user.groups.add(group)
        if not self.alias:
            while True:
                new_alias = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                if not Merchant.objects.filter(alias=new_alias).exists():
                    break
            self.alias = new_alias
        super().save(*args, **kwargs)

class Payment(models.Model):
    card_id = models.CharField(max_length=120, blank=True)
    qr_code = models.ForeignKey(CardHolder, on_delete=models.CASCADE, null=True, blank=True)
    wallet_id = models.ForeignKey(Merchant,on_delete=models.CASCADE,to_field='wallet_id')
    amount = models.DecimalField(max_digits=250,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    commission_fee = models.DecimalField(max_digits=250,decimal_places=2,default=0)
    modified_at = models.DateTimeField(auto_now=True)

    def get_cardholder(self):
        try:
            return CardHolder.objects.get(card_id=self.card_id)
        except CardHolder.DoesNotExist:
            return CardHolder.objects.get(qr_code=self.qr_code)

    def __str__(self):
        cardholder = self.get_cardholder()
        return f"{self.amount} was paid to {self.wallet_id.name} by {self.CardHolder.name}"
