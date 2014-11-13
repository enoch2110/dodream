# -*- coding: utf-8 -*-
import os
import uuid
from django.contrib.auth.models import User
from django.db import models
import datetime


# Create your models here.


def get_filename(filename):
    ext = filename.split('.')[-1].lower()
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename


def get_upload_path(instance, filename):
    return os.path.join('main', isinstance.type, get_filename(filename))


class Entry(models.Model):

    choices = [('notice', u'공지사항'), ('gallery', u'학원소식'), ('reference', u'기타자료')]

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    content = models.TextField()
    writer = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, blank=True, choices=choices)