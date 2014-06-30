from django.contrib.auth.models import User
from django.db import models
import datetime


class Student(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="academy/student")
    gender = models.BooleanField()
    birthday = models.DateField()
    email = models.EmailField()
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    attend_method = models.IntegerField()
    use_sms = models.BooleanField()
    registered_date = models.DateField(default=datetime.date.today())
    information = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User)


class Guardian(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=20, blank=True, null=True)
    relation = models.CharField(max_length=100)
    student = models.ForeignKey(Student)
    user = models.OneToOneField(User)