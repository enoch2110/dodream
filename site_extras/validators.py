# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator


class PhoneNumberValidator(RegexValidator):
    regex = r'01[0-9]{8,9}$'
    message = "정확한 휴대번호를 넣어주세요."