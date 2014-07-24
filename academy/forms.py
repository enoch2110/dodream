# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from academy.models import *


class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academy


class UserCreateMixin(object):
    class Meta:
        exclude = ['profile']

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("Username exists already!")
        return data

    def save(self, commit=True):
        instance = super(UserCreateMixin, self).save(commit=commit)
        if not instance.profile.user:
            instance.profile.user = User.objects.create_user(self.cleaned_data['username'], "", self.cleaned_data['username'])
            instance.profile.save()
        return instance


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['profile', 'academy']

    def clean_contact(self):
        data = self.cleaned_data['contact']
        return data.replace('-', "")


class StudentFilterForm(forms.Form):
    ATTEND_METHOD_CHOICES = [('', "필터안함"), (1, "도보"), (2, "통학버스")]
    IS_PAID_CHOICES = [('', "필터안함"), (True, "지불"), (False, "미지불")]
    COURSE_CHOICES = [('', "필터안함")]

    attend_method = forms.ChoiceField(label="등원수단", choices=ATTEND_METHOD_CHOICES, required=False)
    is_paid = forms.ChoiceField(label="지불여부", choices=IS_PAID_CHOICES, required=False)
    course = forms.ChoiceField(label="수강과목", choices=COURSE_CHOICES, required=False)
    search = forms.CharField(label="검색", required=False)


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['profile', 'academy']

    def clean_contact(self):
        data = self.cleaned_data['contact']
        return data.replace('-', "")


class StaffAuthenticationForm(AuthenticationForm):

    def clean(self):
        cleaned_data = super(StaffAuthenticationForm, self).clean()
        username = cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            profile, created = Profile.objects.get_or_create(user=user)
            if not profile.can_use_admin():
                msg = u"권한이 부족합니다."
                self._errors["username"] = self.error_class([msg])
        return cleaned_data


class GuardianForm(forms.ModelForm):

    class Meta:
        model = Guardian
        exclude = ['student', 'profile']

    def clean_contact(self):
        data = self.cleaned_data['contact']
        return data.replace('-', "")


class CourseForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        leaves = []
        for course_category in CourseCategory.objects.all():
            if course_category.is_leaf():
                leaves.append(course_category.id)
        self.fields['category'] = forms.ModelChoiceField(queryset=CourseCategory.objects.filter(id__in=leaves))

    class Meta:
        model = Course
        exclude = ['is_active']


class LectureForm(forms.ModelForm):

    class Meta:
        model = Lecture


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
