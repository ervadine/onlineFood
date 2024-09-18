from django.urls import path
from .views import register,login, alert_message,logout,myAccount,customer, admin, restaurant
app_name= 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
     path('login/', login, name='login'),
     path('logout/',logout,name="logout"),
      path('myAccount/',myAccount,name="myAccount"),
     path('customer/', customer, name='customer'),
     path('restaurant/',restaurant , name='restaurant'),
     path('admin/', admin, name='admin'),
      
]
