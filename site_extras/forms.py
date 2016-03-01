# -*- coding: utf-8 -*-
from ckeditor.widgets import CKEditorWidget

from django import forms
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from site_extras.fields import SMSCodeField
from site_extras.models.sitemodels import Inquiry, Setting
from site_extras.models.utilmodels import SMSVerification
from django.utils.translation import ugettext_lazy as _


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        exclude = ['is_answered']
        labels = {
            "name": _(u"이름"),
            "contact": _(u"연락처"),
            "email": _(u"이메일"),
            "title": _(u"제목"),
            "content": _(u"내용"),
        }


class SettingForm(forms.ModelForm):

    class Meta:
        model = Setting
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        if self.instance.is_richtext:
            self.fields['content'].widget = CKEditorWidget()


class SMSVerificationFormMixin(forms.ModelForm):
    code = forms.CharField(label="인증번호", required=False, help_text="전송된 인증번호를 입력하세요")
    no_duplicates = False
    is_sms_verification_required = False

    def __init__(self, *args, **kwargs):
        super(SMSVerificationFormMixin, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(SMSVerificationFormMixin, self).save(commit)
        phone_number = self.cleaned_data[self.Meta.phone_number_field]
        code = self.cleaned_data['code']

        if self.is_sms_verification_required:
            verification = SMSVerification.objects.get(phone_number=phone_number, code=code)
            verification.is_verified = True
            verification.save()
        return user

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            verification = SMSVerification.active_objects.get(code=code)
            has_verified_number = SMSVerification.objects.filter(phone_number=verification.phone_number, is_verified=True).exists()
            if has_verified_number and self.no_duplicates:
                raise forms.ValidationError(_(u'이미 인증된 번호입니다.'), code='verified number')
        except MultipleObjectsReturned:
            raise forms.ValidationError(_(u'오류'), code='multiple code')
        except ObjectDoesNotExist:
            pass
        return code

    def clean(self):
        cleaned_data = super(SMSVerificationFormMixin, self).clean()
        old_phone_number = self.initial.get(self.Meta.phone_number_field)
        phone_number = cleaned_data.get(self.Meta.phone_number_field)
        code = cleaned_data.get("code")

        self.is_sms_verification_required = not old_phone_number or (old_phone_number and not old_phone_number == phone_number)
        if self.is_sms_verification_required:
            if not code:
                msg = u"휴대폰번호를 인증하세요."
                self.add_error('code', msg)

            if code and not SMSVerification.active_objects.filter(phone_number=phone_number, code=code).exists():
                msg = u"올바르지 않는 인증번호입니다."
                self.add_error('code', msg)