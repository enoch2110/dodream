from django import forms
from academy.models import Student


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student