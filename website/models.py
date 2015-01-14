# -*- coding: utf-8 -*-
import os
import uuid
from django.contrib.auth.models import User
from django.db import models
import datetime

def get_filename(filename):
    ext = filename.split('.')[-1].lower()
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename


def get_upload_path(instance, filename):
    return os.path.join('main', instance.type, get_filename(filename))


class Entry(models.Model):

    choices = [('notice', u'공지사항'), ('gallery', u'학원소식'), ('reference', u'기타자료')]

    title = models.CharField(max_length=200)
    # file = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    content = models.TextField()
    writer = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, choices=choices)

    def get_main_image(self):
        if self.entryfile_set.all().exists():
            return self.entryfile_set.all()[0].file
        else:
            return None


def get_entryfile_upload_path(instance, filename):
    return os.path.join('main', instance.entry.type, get_filename(filename))


class EntryFile(models.Model):
    file = models.FileField(upload_to=get_entryfile_upload_path)
    entry = models.ForeignKey("Entry")


class EntryComment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    entry = models.ForeignKey("Entry", related_name="comments")