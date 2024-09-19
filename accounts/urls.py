from django.urls import path
from .views import register,login, alert_message,new_password,logout,myAccount,forgot_password,customer,admin, restaurant,activate,success,register_seller
app_name= 'accounts'

urlpatterns = [
     path('register/', register, name='register'),
     path('login/', login, name='login'),
     path('logout/',logout,name="logout"),
     path('myAccount/',myAccount,name="myAccount"),
     path('customer/', customer, name='customer'),
     path('restaurant/',restaurant , name='restaurant'),
     path('admin/', admin, name='admin'),
     path('activate/<uidb64>/<token>',activate, name='activate'),
     path('success/',success, name="success"),
     path('register_seller/', register_seller, name='register_seller'),
     path('new_password/<uidb64>/<token>',new_password, name='new_password'),
     path('forgot_password/',forgot_password, name='forgot_password'),
    
     
      
]
