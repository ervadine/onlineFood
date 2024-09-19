from django.contrib import admin
from .models import User, UserProfile, Seller
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomAdmin(UserAdmin):
    filter_horizontal=()
    list_filter=()
    fieldsets=()
    

admin.site.register(User, CustomAdmin)
admin.site.register(UserProfile)


class SellerInfo(admin.ModelAdmin):
    list_display =('user','seller_name','is_approved','created_at')
    

    
admin.site.register(Seller,SellerInfo)

