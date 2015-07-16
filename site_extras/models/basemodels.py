# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from site_extras.libraries.utils import FilenameChanger


class BaseMedia(models.Model):
    video = models.CharField(max_length=100, blank=True, verbose_name="유튜브 아이디")
    image = models.ImageField(upload_to=FilenameChanger("main/media"), blank=True, verbose_name="이미지")

    class Meta:
        abstract = True

    def clean(self):
        if not (self.image or self.video):
            raise ValidationError("이미지와 비디오 중에 하나는 필요합니다.")
        if self.image and self.video:
            raise ValidationError("이미지와 비디오 중에 하나만 필요합니다.")