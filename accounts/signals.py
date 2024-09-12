from .models import UserProfile, User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver



@receiver(post_save,sender=User)
def build_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('profile created')
    
    else:
        
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
            
        except:
            UserProfile.objects.create(user=instance)
            
      
        
        
@receiver (pre_save,sender=User)     
def pre_save_profile(sender, instance, **kwargs):
    print(f'Instance {instance.username} saved')
    