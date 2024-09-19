from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings

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
    
    
    
        
    
    
def send_verification_email(request,user):
    from_email=settings.DEFAULT_FROM_EMAIL
    current_site=get_current_site(request)
    mail_subject="Please activate your account"
    message=render_to_string('accounts/verification_email.html',{
        'user':user,
        'domain':current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
    })
    to_email=user.email #email
    mail=EmailMessage(mail_subject,message,from_email, to=[to_email])
    mail.send()
    
    
def send_password_reset_email(request,user):
    from_email=settings.DEFAULT_FROM_EMAIL
    current_site=get_current_site(request)
    mail_subject="Password reset request"
    message=render_to_string('accounts/password_reset_email.html',{
        'user':user,
        'domain':current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
    })
    to_email=user.email #email
    mail=EmailMessage(mail_subject,message,from_email, to=[to_email])
    mail.send()
    
    
    