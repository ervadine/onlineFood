from django.db import models
from accounts.models import User, UserProfile

# Create your models here.


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
