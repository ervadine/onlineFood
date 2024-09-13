from django.contrib import admin
from .models import Seller
# Register your models here.

class SellerInfo(admin.ModelAdmin):
    list_display =('user','seller_name','is_approved','created_at')
    

    
admin.site.register(Seller,SellerInfo)