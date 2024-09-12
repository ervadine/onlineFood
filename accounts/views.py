from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm
from .models import User
from django.contrib import messages
# Create your views here.
def register(request):
    if request.method=='POST':
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
    return render(request,'register.html',context)






def login(request):
    return render(request, 'login.html')
def alert_message(request):
    return render(request, 'alert.html')