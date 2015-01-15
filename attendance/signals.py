from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from academy.models import Profile
from attendance.models import AttendanceManager


@receiver(post_save, sender=Profile)
def create_attendance_manager(sender, instance, created, *args, **kwargs):
    if created or not AttendanceManager.objects.filter(profile=instance).exists():
        attendance_manager = AttendanceManager(profile=instance)
        attendance_manager.save()