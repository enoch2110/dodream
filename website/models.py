from django.db import models

# Create your models here.


class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="photo")
    context = models.CharField(max_length=2000)