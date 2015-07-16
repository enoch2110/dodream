# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.forms import MultiWidget
from django.utils.translation import gettext as _
from site_extras.models.utilmodels import SMSVerification
from site_extras.widgets import SMSValidateWidget


class SMSCodeField(forms.Field):

    def clean(self, value):
        try:
            verification = SMSVerification.active_objects.get(code=value)
            if SMSVerification.objects.filter(phone_number=verification.phone_number, is_verified=True).exists():
                raise ValidationError(_('이미 인증된 번호입니다.'), code='verified number')
        except MultipleObjectsReturned:
            raise ValidationError(_('오류'), code='multiple code')
        except ObjectDoesNotExist:
            pass
        return super(SMSCodeField, self).clean(value)


class SMSValidatedField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        self.widget = SMSValidateWidget(
            subfield_1_attrs=kwargs.pop("subfield_1_attrs"),
            subfield_2_attrs=kwargs.pop("subfield_2_attrs")
        )
        error_messages = {
            'incomplete': 'Enter a country calling code and a phone number.',
        }
        fields = (
            forms.CharField(),
            forms.CharField(),
        )
        super(SMSValidatedField, self).__init__(error_messages=error_messages, fields=fields, *args, **kwargs)

    def compress(self, data_list):
        return data_list[0]

    def clean(self, values):
        super(SMSValidatedField, self).clean(values)
        phone_number = values[0]
        code = values[1]

        try:
            verification = SMSVerification.active_objects.get(code=code)
            if SMSVerification.objects.filter(phone_number=verification.phone_number, is_verified=True).exists():
                self.add_error('already verified', '이미 인증된 번호입니다.')
        except MultipleObjectsReturned:
            self.add_error('multiple code', "오류")
        except ObjectDoesNotExist:
            pass

        if code and not SMSVerification.active_objects.filter(phone_number=phone_number, code=code).exists():
            self.add_error('invalid code', "올바르지 않는 인증번호입니다.")

    def get_name(self):
        return "hello"