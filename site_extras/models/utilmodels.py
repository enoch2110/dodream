# -*- coding: utf-8 -*-

from random import randint
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from site_extras.managers import SMSVerificationManager
from site_extras.validators import PhoneNumberValidator


class SMSVerification(models.Model):
    phone_number = models.CharField(max_length=100, validators=[PhoneNumberValidator()])
    code = models.CharField(max_length=10)
    datetime = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    objects = models.Manager()
    active_objects = SMSVerificationManager()

    class Meta:
        verbose_name = "문자인증내역"
        verbose_name_plural = "문자인증내역"

    @classmethod
    def create(cls, number):
        verification = cls(phone_number=number)
        messages = ""
        try:
            verification.full_clean(exclude=['code'])
            messages = "인증번호가 전송되었습니다."
            verification.save()
        except ValidationError as e:
            for arg in e.message_dict:
                for message in e.message_dict[arg]:
                    messages += message + "\n"
            verification = None
        return verification, messages

    @staticmethod
    def is_verified_number(number):
        return SMSVerification.objects.filter(phone_number=number, is_verified=True).exists()

    def save(self, *args, **kwargs):

        if not self.pk:
            verification_in_progress = SMSVerification.active_objects.filter(phone_number=self.phone_number).exists()
            if verification_in_progress:
                return
            else:
                while True:
                    code = str(randint(10000, 99999))
                    if not SMSVerification.active_objects.filter(code=code).exists():
                        break
                self.code = code

        super(SMSVerification, self).save(*args, **kwargs)
