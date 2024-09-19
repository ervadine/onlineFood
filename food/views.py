from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from accounts.models import User, UserProfile
from django.contrib import messages

# Create your views here.

def home(request):
     return render(request, 'food/index.html')


