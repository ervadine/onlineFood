from django.urls import path
from .views import register,login, alert_message
app_name= 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
     path('login/', login, name='login'),
     path('success/', alert_message, name='success'),
]
