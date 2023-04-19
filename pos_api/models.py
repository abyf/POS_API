from django.db import models
import uuid,random,string
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group


class Manager(models.Model):
    username = models.CharField(max_length=120, unique=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120,null=True, blank=True)
    email = models.EmailField(max_length=120,null=True, blank=True)
    cardholder_commission = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    merchant_commission = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{username}:{balance}".format(username=self.username,balance=self.balance)

class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrators')
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120,null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=120,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return "{name}".format(name=self.name)

    def save(self,*args,**kwargs):
        if not self.pk:
            #If this is a new Administrator, add them to the Administrator Group
            group = Group.objects.get(name='administrators')
            self.user.groups.add(group)
        #if the user has been used, disable it before saving
        if Administrator.objects.filter(user=self.user).exclude(pk=self.pk).exists():
            self.user.is_active = False
            self.user.save()
        super().save(*args, **kwargs)

class CardHolder(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120,null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=120, null=True, blank=True)
    card_id = models.UUIDField(default=uuid.uuid4,editable=False, unique=True,null=True, blank=True)
    qr_code = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    alias = models.CharField(max_length=8,unique=True,editable=False)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    qr_code_img = models.ImageField(upload_to='qr_codes/',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    administrator = models.ForeignKey(Administrator, on_delete=models.SET_NULL,null=True,blank=True, verbose_name='Created_by')
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
    phone = models.CharField(max_length=120,null=True, blank=True)
    address = models.CharField(max_length=250,null=True, blank=True)
    email = models.EmailField(max_length=120,null=True, blank=True)
    reader_id = models.CharField(max_length=50,null=True, blank=True, unique=True)
    wallet_id = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    alias = models.CharField(max_length=8,unique=True,editable=False)
    balance = models.DecimalField(max_digits=250,decimal_places=2,default=0,editable=False)
    is_active = models.BooleanField(default=True)
    administrator = models.ForeignKey(Administrator, on_delete=models.SET_NULL,null=True,blank=True,verbose_name='Created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE,default=2)

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

class Transaction(models.Model):
    TRANSACTION_TYPES = [('load','Load'),('withdraw','Withdraw')]
    transaction_type = models.CharField(choices=TRANSACTION_TYPES,max_length=10)
    cardholder_alias = models.CharField(max_length=8,null=True,blank=True)
    card_id = models.UUIDField(null=True, blank=True)
    qr_code = models.UUIDField(null=True, blank=True)
    merchant_alias = models.CharField(max_length=8,null=True,blank=True)
    amount = models.DecimalField(max_digits=250,decimal_places=2,null=True, blank=True)
    administrator = models.ForeignKey(Administrator, on_delete=models.SET_NULL,null=True,blank=True,verbose_name='Performed_by')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_name(self):
        if self.cardholder_alias:
            return CardHolder.objects.get(alias=self.cardholder_alias).name
        elif self.card_id:
            return CardHolder.objects.get(card_id=self.card_id).name
        elif self.qr_code:
            return CardHolder.objects.get(qr_code=self.qr_code).name
        elif self.merchant_alias:
            return Merchant.objects.get(merchant_alias=self.merchant_alias).name
        else:
            return None

    def __str__(self):
        name = self.get_name()
        if name:
            return "{cardholder} credited FCFA {amount} on {date}".format(cardholder=name,amount=self.amount,date=self.created_at.strftime("%Y-%m-%d%H%M%S"))
        else:
            return "REQUESTER UNKNOWN"

    def clean(self):
        if not any([self.cardholder_alias,self.card_id,self.qr_code]):
            raise ValidationError("At least one of the fields 'cardholder_alias', 'card_id', or 'qr_code' must be provided.")
        if self.cardholder_alias and not CardHolder.objects.filter(alias=self.cardholder_alias).exists():
            raise ValidationError("Cardholder with alias {} does not exist.".format(self.cardholder_alias))
        if self.merchant_alias and not Merchant.objects.filter(alias=self.merchant_alias).exists():
            raise ValidationError("Merchant with alias {} does not exist.".format(self.merchant_alias))
        if self.card_id and not CardHolder.objects.filter(card_id=self.card_id).exists():
            raise ValidationError("Cardholder with Card ID {} does not exist.".format(self.card_id))
        if self.qr_code and not CardHolder.objects.filter(qr_code=self.qr_code).exists():
            raise ValidationError("Cardholder with QR code {} does not exist.".format(self.qr_code))

    def save(self,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)

class Payment(models.Model):
    card_id = models.UUIDField(null=True, blank=True)
    qr_code = models.UUIDField(null=True, blank=True)
    wallet_id = models.ForeignKey(Merchant,on_delete=models.CASCADE,to_field='wallet_id',verbose_name='To_Merchant')
    amount = models.DecimalField(max_digits=250,decimal_places=2,default=0)
    commission_fee = models.DecimalField(max_digits=250,decimal_places=2,default=0)
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
