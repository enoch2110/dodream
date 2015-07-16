# -*- coding: utf-8 -*-
from django.db import models
from site_extras.libraries.utils import FilenameChanger
from django.utils.translation import ugettext_lazy as _


class Inquiry(models.Model):
    name = models.CharField(max_length=100, verbose_name="작성자")
    contact = models.CharField(max_length=100, verbose_name="연락처")
    email = models.EmailField(verbose_name="이메일")
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="문의내용")
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    is_answered = models.BooleanField(default=False, verbose_name="답변여부")

    class Meta:
        verbose_name = _(u"문의사항")
        verbose_name_plural = _(u"문의사항")


class Popup(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    datetime = models.DateTimeField(auto_now=True)
    date_begin = models.DateField()
    date_end = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _(u"팝업")
        verbose_name_plural = _(u"팝업")


class Setting(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"설정명", unique=True)
    type = models.CharField(max_length=100, blank=True, verbose_name=u"설정 종류")
    help_text = models.TextField(blank=True, verbose_name=u"설명")
    is_richtext = models.BooleanField(default=False, verbose_name=u"리치텍스트")
    content = models.TextField(blank=True, verbose_name=u"내용")

    class Meta:
        verbose_name = _(u"사이트 설정")
        verbose_name_plural = _(u"사이트 설정")


class SettingFile(models.Model):
    file = models.FileField(upload_to=FilenameChanger("site_extras/settings"), blank=True, verbose_name=u"파일")
    content = models.TextField(blank=True)
    setting = models.ForeignKey(Setting, related_name="files")