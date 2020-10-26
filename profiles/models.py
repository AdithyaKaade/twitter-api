from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
# Create your models here.

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	followers = models.ManyToManyField(User, related_name='following', blank=True)

    
 #   project_obj = Profile.objects.first()
 #   project_obj.followers.all() -> All users following this profile
 #   user.following.all() -> All user profiles I follow
    

def user_did_save(sender, instance, created, *args, **kwargs):
	if created:
		Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)