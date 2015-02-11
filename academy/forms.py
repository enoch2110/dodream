# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from academy.models import *
from django.db.models import Q
from django.forms import CheckboxSelectMultiple


class AcademyForm(forms.ModelForm):
    #opening_time = forms.DateField()

    class Meta:
        model = Academy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AcademyForm, self).__init__(*args, **kwargs)
        settings = Setting.objects.filter(academy=self.instance)


class UserCreateMixin(object):
    class Meta:
        fields = '__all__'
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
        exclude = ['profile', 'academy', 'textbook']

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
        fields = '__all__'
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
        fields = '__all__'
        exclude = ['student', 'profile']

    def clean_contact(self):
        data = self.cleaned_data['contact']
        return data.replace('-', "")


class CategoryCreateForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['academy']


class SubjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


class StudentSubjectForm(forms.ModelForm):
    class Meta:
        model = StudentSubject
        fields = '__all__'
        exclude = ['student']


########################################################################################################################
# class CourseForm(forms.ModelForm):
#
#     def __init__(self,  *args, **kwargs):
#         super(CourseForm, self).__init__(*args, **kwargs)
#         leaves = []
#         for course_category in CourseCategory.objects.all():
#             if course_category.is_leaf():
#                 leaves.append(course_category.id)
#         self.fields['category'] = forms.ModelChoiceField(queryset=CourseCategory.objects.filter(id__in=leaves))
#
#     class Meta:
#         model = Course
#         fields = '__all__'
#         exclude = ['is_active', 'academy']
#
#
# class CourseCategoryForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         academy = self.self.request.user.profile.staff.academy
#         super(CourseCategoryForm, self).__init__(*args, **kwargs)
#         self.category['parent'].queryset = academy.get_parents()
#
#     class Meta:
#         model = CourseCategory
#         fields = '__all__'
#
#
# class LectureForm(forms.ModelForm):
#
#     class Meta:
#         model = Lecture
#         fields = '__all__'
#         widgets = {
#             'weekday': CheckboxSelectMultiple,
#         }
#         exclude = ['students', 'is_active']
#         unique_together = ("code", "course__academy")
#
#     def __init__(self, *args, **kwargs):
#         academy = kwargs.pop("academy")
#         super(LectureForm, self).__init__(*args, **kwargs)
#         self.fields['staffs'].queryset = academy.get_staffs()
#         self.fields['course'].queryset = academy.get_courses()
#
#
# class LectureRegistrationForm(forms.ModelForm):
#     students = forms.ModelMultipleChoiceField(queryset=Student.objects.none())
#
#     class Meta:
#         model = Lecture
#         fields = '__all__'
#         exclude = ['code', 'course', 'staff', 'is_online', 'weekday', 'is_active']
#
#     def __init__(self, *args, **kwargs):
#         super(LectureRegistrationForm, self).__init__(*args, **kwargs)
#         #TODO academy specific
#         #students.filter(~Q(id__in=self.instance.students.all()))
#
#         self.fields['students'].queryset = Student.objects.filter(~Q(id__in=self.instance.students.all()))
#
#
# class PaymentForm(forms.ModelForm):
#
#     class Meta:
#         model = Payment
#         fields = '__all__'
#
#
# class TextbookForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ("name", "textbook")