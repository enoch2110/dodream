from django.shortcuts import render
from django.views.generic import View, CreateView
from academy.forms import StudentCreateForm
from academy.models import Student


class StudentRegistration(CreateView):
    model = Student
    template_name = "student-add.html"
    form_class = StudentCreateForm