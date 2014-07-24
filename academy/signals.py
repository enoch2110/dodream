from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from academy.models import Profile, Student, Staff, Guardian


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created or not Profile.objects.filter(user=instance).exists():
        profile = Profile(user=instance)
        profile.save()


@receiver(post_delete, sender=Guardian)
@receiver(post_delete, sender=Staff)
@receiver(post_delete, sender=Student)
def delete_user(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()

