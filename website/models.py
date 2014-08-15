from django.db import models

# Create your models here.


class Notice(models.Model):
    title = models.TextField(max_length=100)
    content = models.TextField(max_length=2000)
    writer = models.TextField(max_length=30)