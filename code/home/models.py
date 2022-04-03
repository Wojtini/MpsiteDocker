from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user} Profile"

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    quote_text = models.TextField()

    def __str__(self):
        return f'{self.user} ~ "{self.quote_text}"'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



admin.site.register(Profile)
admin.site.register(Quote)
