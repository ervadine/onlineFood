from typing import Any
from django import forms
from .models import User, UserProfile,Seller


class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    cpassword=forms.CharField(widget=forms.PasswordInput())
   
    class Meta:
        model=User
        fields=('first_name','last_name','password','username','email','phone','role')
    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        password = cleaned_data.get('password')
        cpassword = cleaned_data.get('cpassword')
        if password!=cpassword:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
    
class UserProfileForm(forms.ModelForm):
   
    
    class Meta:
        model=UserProfile
        fields=('profile_picture','cover_photo','address_line_1','address_line_2','city','country','state','pin_code','longitude','latitude')


class SellerForm(forms.ModelForm):

   
    class Meta:
        model=Seller
        fields=('seller_name','seller_license')