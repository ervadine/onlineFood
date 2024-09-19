from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import RegisterForm, SellerForm
from .models import User, UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from .utils import check_role_user, role_admin,role_customer,role_vendor, send_verification_email,send_password_reset_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator



#seller registration

def register_seller(request):
     
     user_form=RegisterForm(request.POST)
     seller_form=SellerForm(request.POST, request.FILES)
     
     if request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,'you are already logged in')
        return redirect('accounts:myAccount')
     
     elif request.method=='POST' :
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
             send_verification_email(request,user)
             seller=seller_form.save(commit=False)
             
             if 'seller_license' in request.FILES:
                   seller.seller_license=request.FILES['seller_license']
                   seller.user=user
                   user_profile=UserProfile.objects.get(user=user)
                   seller.user_profile=user_profile
                   seller.save()
                   
                   messages.success(request,"your request has been saved successfully. Wait for approval",fail_silently=True)
                   redirect("accounts:login")
             else:
                  messages.error(request, "Please upload a valid seller license.",fail_silently=True)
                  return redirect("accounts:register_seller")
             
         
         
     else:
       user_form=RegisterForm()
       seller_form=SellerForm()
     context={"seller_form":seller_form,"user_form":user_form}
     return render(request, 'accounts/register_seller.html', context)


# Create your views here.
def register(request):
    if request.user.is_authenticated:
           messages.add_message(request,messages.WARNING,'you are already logged in')
          
           return redirect('accounts:myAccount')
       
    elif request.method=='POST':
        form=RegisterForm(request.POST)
        try:
          if form.is_valid():
            #create user using form data and set password securely
            # password=form.cleaned_data.get('password')
            # user=form.save(commit=False)
            # user.set_password(password)
            # user.role=User.CUSTOMER
            # user.save()
            #----------------------------------------------------
            #create user user create_user method in User model
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            email=form.cleaned_data.get('email')
            username=form.cleaned_data.get('username')
            phone=form.cleaned_data.get('phone')
            password=form.cleaned_data.get('password')
           
            user=User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name,phone=phone)
            user.set_password(password)  # set password securely
            user.role=User.CUSTOMER  # set user role as customer
            user.save()  # save user to database
            send_verification_email(request,user)
            success_message = f" {first_name} 's account was created successfully"
            messages.success(request,success_message, fail_silently=True)
            return redirect('accounts:success')  # Redirect to a success page.
          else:
               error_message ="some error occurred"
               print(error_message)
            
        except Exception as e:
            raise e
            
        
    else:
        form=RegisterForm()
    context={'form': form}
    return render(request,'accounts/register.html',context)






def login(request):
 if request.user.is_authenticated:
     messages.warning(request,'you are already logged in')
     
     return redirect('accounts:myAccount')
    
 elif request.method=="POST":
    email=request.POST.get('email')
    password=request.POST.get('password')
    user=authenticate(email=email,password=password)
    if user:
        
         if user.is_active:
                 auth_login(request,user)
                 messages.success(request,"you are logged in successfully.")
                 
                 return redirect('accounts:myAccount') # Redirect to a success page.
         else:
              messages.warning(request,"Your account's status is not active yet.")
              return redirect('accounts:login') # Redirect to
    else:
         
         messages.warning(request,"Invalid credentials, maybe your account's status is not active yet.")
    
        
    
 return render(request,'accounts/login.html',{})



def alert_message(request):
    return render(request, 'alert.html')


@login_required(login_url="accounts:login")
def logout(request):
    auth_logout(request)
    messages.add_message(request,messages.SUCCESS,"You successfully logged out")
    return render(request, 'accounts/login.html')



@login_required(login_url="accounts:login")
def myAccount(request):
    page_url=check_role_user(request.user)
    return redirect(page_url)
    
@login_required(login_url='accounts:login')
@user_passes_test(role_vendor)
def restaurant(request):
    return render(request, 'accounts/restaurant_dashboard.html')


@login_required(login_url='accounts:login')
@user_passes_test(role_customer)
def customer(request):
    return render(request, 'accounts/customer_dashboard.html')



@login_required(login_url='accounts:login')
@user_passes_test(role_admin)
def admin(request):
    return render(request, 'accounts/dashboard.html')

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode('utf8')
        user=User.objects.get(pk=uid)
        
        if user.is_active:
            messages.warning(request,"Your account is already active.")
            return redirect('accounts:login')
        
        if user.is_verified:
            messages.warning(request,"Your account is already verified.")
            return redirect('accounts:login')
        
        if user is not None and default_token_generator.check_token(user,token):
            user.is_verified=True
            user.is_admin=True
            user.is_staff=True
            user.is_active=True  # set user as active after verification
            user.save()
            messages.success(request,"Your account has been successfully verified.")
            return redirect('accounts:login')
        
    except (TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None
        messages.warning(request,"Verification failed.")
        return redirect('accounts:login')

def success(request):
    return render(request,'accounts/success.html')


def forgot_password(request):
    if request.method=='POST':
        email=request.POST.get('email')
        user=User.objects.filter(email=email).first()
        if user:
            send_password_reset_email(request,user)
            messages.success(request,"We have sent a password reset link to your email.")
            return redirect('accounts:myAccount')
        else:
            messages.error(request,"No account found with this email.")
            return redirect('accounts:forgot_password')
    return render(request,'accounts/forgot_password.html')

def new_password(request,uidb64,token):
    if request.method=='POST':
        
        new_password=request.POST.get('password')
        try:
            uid=urlsafe_base64_decode(uidb64).decode('utf8')
            user=User.objects.get(pk=uid)
            
            if user is not None and default_token_generator.check_token(user,token):
                user.set_password(new_password)
                user.save()
                messages.success(request,"Your password has been changed successfully.")
                return redirect('accounts:myAccount')
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            messages.error(request,"Password reset failed.")
            return redirect('accounts:forgot_password')
    
    return render(request,'accounts/new_password.html')





