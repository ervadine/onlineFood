from typing import Any
from django import forms
from accounts.models import User, UserProfile
from .models import Seller


class SellerForm(forms.ModelForm):

   
    class Meta:
        model=Seller
        fields=('seller_name','seller_license')

    
    
