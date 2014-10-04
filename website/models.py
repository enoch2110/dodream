import datetime
from django.db import models

# Create your models here.


class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="photo")
    context = models.CharField(max_length=2000)


class Notice(models.Model):
    number = models.IntegerField(max_length=5, default=1)
    subject = models.CharField(max_length=200)
    file = models.FileField(upload_to="notice", blank=True, null=True)
    text = models.TextField()
    writer = models.CharField(max_length=20)
    date = models.DateField(default=datetime.date.today())

    def __unicode__(self):
        return self.subject