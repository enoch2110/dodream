from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from academy.models import Profile, Student, Staff, Guardian


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created or not Profile.objects.filter(user=instance).exists():
#         profile = Profile(user=instance)
#         profile.save()


@receiver(pre_save, sender=Guardian)
@receiver(pre_save, sender=Staff)
@receiver(pre_save, sender=Student)
def create_profile(sender, instance, *args, **kwargs):
    if not instance.pk or not instance.profile:
        profile = Profile()
        profile.save()
        instance.profile = profile
