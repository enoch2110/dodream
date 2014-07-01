from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.views.generic import View, CreateView
from academy.forms import StudentCreateForm, GuardianForm
from academy.models import Student


class StudentRegistration(CreateView):
    model = Student
    template_name = "student-add.html"
    form_class = StudentCreateForm

    def get_context_data(self, **kwargs):
        context = super(StudentRegistration, self).get_context_data(**kwargs)
        GuardianFormSet = formset_factory(GuardianForm, extra=4)
        context['formset'] = GuardianFormSet
        return context

    # def get(self, request, *args, **kwargs):
    #
    #
    #     return super(StudentRegistration, self).get(request)