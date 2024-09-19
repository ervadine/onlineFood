from django.urls import path
from .views import home


app_name= 'food'

urlpatterns = [
    path('home/', home, name='home')
]
