from django import forms
from academy.models import Student, Guardian


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user']


class GuardianForm(forms.ModelForm):

    class Meta:
        model = Guardian
        exclude = ['student', 'user']
