# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import CheckboxSelectMultiple
from academy.models import Student, Guardian, CourseCategory, Course, Staff, Profile, Academy, Lecture


class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academy


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'academy']

    def clean_contact(self):
        data = self.cleaned_data['contact']
        return data.replace('-', "")


class StaffForm(forms.ModelForm):

    class Meta:
        model = Staff
        exclude = ['user', 'academy']

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
        exclude = ['student', 'user']

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
        exclude = ['is_active', 'academy']


class LectureForm(forms.ModelForm):

    class Meta:
        model = Lecture
        widgets = {
            'weekday': CheckboxSelectMultiple,
        }
        exclude = ['students','is_active']


class LectureRegistrationForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.none())

    class Meta:
        model = Lecture
        exclude = ['code', 'course', 'staff', 'is_online', 'weekday', 'is_active']

    def __init__(self, *args, **kwargs):
        super(LectureRegistrationForm, self).__init__(*args, **kwargs)
        #TODO academy specific
        self.fields['students'].queryset = Student.objects.filter(~Q(id__in=self.instance.students.all()))
