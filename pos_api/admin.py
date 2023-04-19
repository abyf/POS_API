from django.contrib import admin,messages
from django.core.exceptions import ValidationError
from django.urls import reverse
from . models import CardHolder, Merchant, Administrator, Manager, Transaction, Payment
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('id','username','is_staff')
    list_filter = ('is_staff','is_superuser','groups')
    search_fields = ('username',)
    ordering = ('username',)
    fieldsets = ((None,{'fields':('username','password')}),('Permissions',{'fields':('is_active','is_staff','groups')}),)
    add_fieldsets = ((None,{'classes':('wide',),'fields':('username','password1','password2','is_staff','groups'),}),)

    def add_view(self,request,form_url='',extra_context=None):
        """Only allow administrators to create users with staff status, not superuser status"""
        self.fieldsets[1][1]['fields'] = ('is_active','is_staff','groups')
        return super().add_view(request,form_url=form_url,extra_context=extra_context)

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('id','username','name','phone','email','cardholder_commission','merchant_commission','balance','created_at', 'modified_at')

class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','address','email','created_at', 'modified_at')

class CardHolderAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','email','card_id','qr_code','balance','alias','created_at', 'modified_at')
    readonly_fields = ('qr_code_img',)

    def get_list_display(self,request):
        if request.user.is_superuser:
            return('id','name','phone','email','card_id','qr_code','alias','qr_code_img','balance','created_at', 'modified_at')
        else:
            return('id','name','phone','email','balance','created_at', 'modified_at')

class MerchantAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','email','reader_id','wallet_id','alias','balance','created_at', 'modified_at')

    def get_list_display(self,request):
        if request.user.is_superuser:
            return('id','name','phone','email','reader_id','wallet_id','alias','balance','created_at', 'modified_at')
        else:
            return('id','name','phone','email','balance','created_at', 'modified_at')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id','transaction_type','name','amount','created_at']
    list_filter = ['transaction_type','created_at']
    search_fields = ['cardholder__card_id','cardholder__qr_code','cardholder__alias','cardholder__name','merchant__alias']

    def get_cardholder_name(self,obj):
        if obj.cardholder_alias:
            return CardHolder.objects.get(alias=obj.cardholder_alias).name
        elif obj.card_id:
            return CardHolder.objects.get(card_id=obj.card_id).name
        elif obj.qr_code:
            return CardHolder.objects.get(qr_code=obj.qr_code).name
        else:
            return "UNKNOWN CARDHOLDER"

    def get_merchant_name(self,obj):
        if obj.merchant_alias:
            return Merchant.objects.get(merchant_alias=obj.merchant_alias).name
        else:
            return "UNKNOWN MERCHANT"

    def name(self,obj):
        if obj.transaction_type == 'load':
            return self.get_cardholder_name(obj)
        else:
            return self.get_merchant_name(obj)

    def clean(self):
        try:
            self.model(**self.cleaned_data).full_clean()
        except ValidationError as e:
            self.add_error(None,e)

    def get_fields(self,request,obj=None):
        fields = ['transaction_type','amount']
        if obj and obj.transaction_type == 'load':
            fields += ['cardholder_alias','card_id','qr_code']
        elif obj and obj.transaction_type == 'withdraw':
            fields += ['merchant_alias']
        elif request.method == 'POST':
            transaction_type = request.POST.get('transaction_type')
            if transaction_type == 'load':
                fields += ['cardholder_alias','card_id','qr_code']
            elif transaction_type == 'withdraw':
                fields += ['merchant_alias']
        return fields

    fieldsets = (
    ('Transaction Details',{'fields':('transaction_type','amount')}),
    ('Cardholder Details',{'fields':('cardholder_alias','card_id','qr_code'),'classes':('collapse',),'description':'Fill in either the alias, card ID or QR code of the cardholder for a load transaction'}),
    ('Merchant Details',{'fields':('merchant_alias',),'classes':('collapse',),'description':'Fill in the alias of the merchant for a withdraw transaction'})
    )

    def save_model(self,request,obj,form,change):
        """ Override the default save_model method to allow admins to load or withdraw money from cardholders and merchants"""
        try:
            obj.full_clean()
            if not change:
                #this is a new transaction
                if obj.transaction_type == 'load':
                    #The admin is adding money to a cardholder's Account
                    try:

                        if obj.cardholder_alias:
                            cardholder=CardHolder.objects.get(alias=obj.cardholder_alias)
                        elif obj.card_id:
                            cardholder=CardHolder.objects.get(card_id=obj.card_id)
                        elif obj.qr_code:
                            cardholder = CardHolder.objects.get(qr_code=obj.qr_code)
                        else:
                            cardholder = None
                        if cardholder:
                            cardholder.balance += obj.amount
                            cardholder.save()
                        else:
                            messages.error(request,'No matching cardholder has been found')
                    except CardHolder.DoesNotExist:
                        messages.error(request,'No matching cardholder has been found')
                elif obj.transaction_type == 'withdraw':
                    try:
                        merchant=Merchant.objects.get(alias=obj.merchant_alias)
                        merchant.balance -= obj.amount
                        merchant.save()
                    except Merchant.DoesNotExist:
                        messages.error(request,'No matching merchant has been found')
            super().save_model(request,obj,form,change)
        except ValidationError as e:
            messages.error(request,e.message_dict)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','card_id','qr_code','wallet_id','amount','commission_fee', 'created_at','modified_at')


admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(CardHolder,CardHolderAdmin)
admin.site.register(Merchant,MerchantAdmin)
admin.site.register(Manager,ManagerAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)
