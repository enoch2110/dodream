from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from academy.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created or not Profile.objects.filter(user=instance).exists():
        profile = Profile(user=instance)
        profile.save()