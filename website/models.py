# -*- coding: utf-8 -*-
import os
import uuid
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models



def get_filename(filename):
    ext = filename.split('.')[-1].lower()
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename


def get_upload_path(instance, filename):
    return os.path.join('main', instance.type, get_filename(filename))


class Entry(models.Model):

    choices = [('notice', u'공지사항'), ('gallery', u'학원소식'), ('reference', u'기타자료')]
    type = models.CharField(max_length=100, choices=choices)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    # file = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    content = RichTextField()
    writer = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)

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

    def get_file(self):
        return self.file


class EntryComment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    entry = models.ForeignKey("Entry", related_name="comments")


def get_carousel_image_upload_path(instance, filename):
    return os.path.join('main', 'carousel', get_filename(filename))


class CarouselItem(models.Model):
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    content = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to=get_carousel_image_upload_path)

    def __unicode__(self):
        return self.title


