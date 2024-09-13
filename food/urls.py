from django.urls import path
from .views import home, register_seller


app_name= 'food'

urlpatterns = [
    path('home/', home, name='home'),
    path('register_seller/', register_seller, name='register_seller')
]
