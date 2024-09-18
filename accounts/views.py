from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import RegisterForm
from .models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from .utils import detectUser
from django.core.exceptions import PermissionDenied

#restrict user from accessing the other pages


def check_role_user(req):
    page_url=''
    if req.is_authenticated:
        if req.role == 2:
            page_url='accounts:customer'
            return page_url
        elif req.role == 1:
            page_url='accounts:restaurant'
            return page_url
        elif req.role == None and req.is_superuser:
            page_url='accounts:admin'
            return page_url
        else:
            page_url='accounts:login'
            return page_url
    else:
        page_url='accounts:login'
        return page_url

def role_vendor(user):
    
    if user.role==1:
        return True
    else:
        raise PermissionDenied
        
        
def role_customer(user):
    if user.role==2:
        return True
    else:
           raise PermissionDenied
        
def role_admin(user):
    if user.is_superuser:
        return True
    else:
           raise PermissionDenied

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






