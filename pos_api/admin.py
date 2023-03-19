from django.contrib import admin
from .models import CardHolder,Merchant
from members.models import User


admin.site.register(CardHolder)
admin.site.register(Merchant)
admin.site.register(User)
