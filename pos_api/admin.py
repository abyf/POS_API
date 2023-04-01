from django.contrib import admin
from .models import CardHolder, Merchant, Manager
from django.utils.html import format_html

class CardHolderAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','email','card_id','qr_code','balance','created_at', 'modified_at')
    readonly_fields = ('qr_code_image',)

    def qr_code_image(self,obj):
        return format_html('<img src="{}" />'.format(obj.get_qr_code_url()))

    qr_code_image.short_description = 'QR Code'
    qr_code_image.allow_tags = True

class MerchantAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','email','reader_id','wallet_id', 'balance','created_at', 'modified_at')

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('id','username','name','phone','email','cardholder_commission','merchant_commission','balance','created_at', 'modified_at')


admin.site.register(CardHolder, CardHolderAdmin)
admin.site.register(Merchant, MerchantAdmin)
admin.site.register(Manager,ManagerAdmin)
