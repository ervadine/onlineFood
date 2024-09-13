from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from .forms import SellerForm
from accounts.models import User, UserProfile
from django.contrib import messages
# Create your views here.

def home(request):
     return render(request, 'index.html')


def register_seller(request):
     
     user_form=RegisterForm(request.POST)
     seller_form=SellerForm(request.POST, request.FILES)
     
     if request.method=='POST' :
          if user_form.is_valid() and seller_form.is_valid():
             first_name=user_form.cleaned_data['first_name']
             last_name=user_form.cleaned_data['last_name']
             email=user_form.cleaned_data['email']
             username=user_form.cleaned_data['username']
             phone=user_form.cleaned_data['phone']
             password=user_form.cleaned_data['password']
             
             user=User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name,phone=phone)
             user.set_password(password)
             user.role=User.RESTAURANT
             user.save()
             
             seller=seller_form.save(commit=False)
             
             if 'seller_license' in request.FILES:
                   seller.seller_license=request.FILES['seller_license']
                   seller.user=user
                   user_profile=UserProfile.objects.get(user=user)
                   seller.user_profile=user_profile
                   seller.save()
                 
                   messages.success(request,"your request has been saved successfully. Wait for approval",fail_silently=True)
                   redirect("food:register_seller")
             else:
                  messages.error(request, "Please upload a valid seller license.",fail_silently=True)
                  return redirect("food:register_seller")
             
         
         
     else:
       user_form=RegisterForm()
       seller_form=SellerForm()
     context={"seller_form":seller_form,"user_form":user_form}
     return render(request, 'register_seller.html', context)