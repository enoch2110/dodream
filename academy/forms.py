from django import forms
from academy.models import Student, Guardian, CourseCategory, Course, Staff


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
        exclude = ['is_active']