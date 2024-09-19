from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, first_name,last_name,email,username,phone,password=None, **kwargs):
     if not email:
         raise ValueError('Email is required')
     if not username:
         raise ValueError('User name is required')
     
     user=self.model(
      email=self.normalize_email(email),
      username=username,
      password=password,
      phone=phone,
      first_name=first_name,
      last_name=last_name
      )
    
     user.set_password(password)
     user.save(using=self._db)
     return user
 
 
    def create_superuser(self, first_name,last_name,email,username,phone,password=None, **kwargs):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name
            )
        
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    RESTAURANT=1
    CUSTOMER=2
    ROLE_CHOICE=((RESTAURANT,'Restaurant'),(CUSTOMER,'Customer'))
    first_name=models.CharField(max_length=50,blank=True)
    last_name=models.CharField(max_length=50,blank=True)
    email=models.EmailField(max_length=100,unique=True)
    phone=models.CharField(max_length=15,blank=True)
    username=models.CharField(max_length=50,unique=True)
    role=models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)
  
    
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    
    is_verified=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name','phone']
    objects=UserManager()
    
    def __str__(self):
        return self.email
    
    def has_permission(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True
    def get_role(self):
        if self.role==1:
            user_role= 'Restaurant'
        elif self.role==2:
              user_role ='Customer'
        return user_role
        
    
    
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='users/profile_images',blank=True,null=True)
    cover_photo=models.ImageField(upload_to='users/cover_images',blank=True,null=True)
    address_line_1=models.CharField(max_length=50,blank=True)
    address_line_2=models.CharField(max_length=50,blank=True)
    city=models.CharField(max_length=50,blank=True)
    country=models.CharField(max_length=50,blank=True)
    state=models.CharField(max_length=50,blank=True)
    pin_code=models.CharField(max_length=50,blank=True)
    longitude=models.CharField(max_length=50,blank=True,)
    latitude=models.CharField(max_length=50,blank=True)
    modified_at=models.DateTimeField(auto_now=True,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    
    def __str__(self):
        return self.user.email
    
    


     
class Seller(models.Model):
    user=models.OneToOneField(User, related_name="user",on_delete=models.CASCADE)
    user_profile=models.OneToOneField(UserProfile,related_name="userprofile", on_delete=models.CASCADE)
    seller_name=models.CharField(max_length=50)
    seller_license=models.ImageField(upload_to="seller/license/")
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.seller_name