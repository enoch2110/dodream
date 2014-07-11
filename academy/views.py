from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView
from rest_framework.filters import SearchFilter
from academy.admin import StudentModelAdmin
from academy.forms import *
from academy.models import *


class StudentRegistration(View):
    template_name = "student-add.html"
    formset_class = formset_factory(GuardianForm)
    form_class = StudentCreateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = self.formset_class()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        formset = self.formset_class(request.POST)
        if form.is_valid() and formset.is_valid():
            student = form.save(commit=False)
            student.academy = request.user.staff.academy
            student.save()
            for form in formset:
                if form.has_changed():
                    guardian = form.save(commit=False)
                    guardian.student = student
                    guardian.save()
            return redirect("student-list")
        return render(request, self.template_name, {'form': form, 'formset': formset},)


class StudentUpdate(View):
    template_name = 'student-update.html'
    formset_class = modelformset_factory(Guardian, form=GuardianForm)
    form_class = StudentCreateForm

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(id=kwargs['pk'])
        form = self.form_class(instance=student)
        formset = self.formset_class(queryset=student.guardian_set.all())
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        student = Student.objects.get(id=kwargs['pk'])
        form = self.form_class(request.POST, request.FILES, instance=student)
        formset = self.formset_class(request.POST, queryset=student.guardian_set.all())
        if form.is_valid() and formset.is_valid():
            student = form.save()
            for form in formset:
                if form.has_changed():
                    guardian = form.save(commit=False)
                    guardian.student = student
                    guardian.save()
            return redirect("student-list")
        return render(request, self.template_name, {'form': form, 'formset': formset},)


class StudentList(ListView):
    template_name = "student-list.html"
    queryset = Student.objects.all()
    context_object_name = "students"

    def get_queryset(self):
        return StudentModelAdmin(Student, None).get_search_results(self.request, self.queryset, self.request.GET.get('q'))[0]


class StaffList(ListView):
    template_name = "staff-list.html"
    queryset = Staff.objects.all()
    context_object_name = "staffs"


class StaffDetail(DetailView):
    template_name = "staff-detail.html"
    context_object_name = "staff"
    model = Staff


class StaffCreate(CreateView):
    template_name = "staff-add.html"
    model = Staff
    form_class = StaffForm
    success_url = "/staff-list"


class StaffUpdate(UpdateView):
    template_name = "staff-update.html"
    model = Staff
    form_class = StaffForm
    success_url = "/staff-list"


class StaffDelete(DeleteView):
    template_name = "staff-delete.html"
    model = Staff
    success_url = "/staff-list"


class CourseCategoryList(ListView):
    template_name = "course-list.html"
    queryset = CourseCategory.objects.filter(parent=None)
    context_object_name = "root_categories"


class CourseCreate(CreateView):
    template_name = "course-add.html"
    model = Course
    form_class = CourseForm
    success_url = "/course-list"


class CourseCategoryCreate(CreateView):
    template_name = "course-category.html"
    model = CourseCategory
    success_url = "/course-category-list"

    def get_context_data(self, **kwargs):
        context = super(CourseCategoryCreate, self).get_context_data(**kwargs)
        context.update({'root_categories': CourseCategory.objects.filter(parent=None)})
        return context