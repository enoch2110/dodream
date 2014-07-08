from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView
from academy.forms import StudentCreateForm, GuardianForm, CourseForm
from academy.models import Student, Course, CourseCategory


class StudentRegistration(View):
    template_name = "student-add.html"
    formset_class = formset_factory(GuardianForm)
    form_class = StudentCreateForm

    def get_context_data(self, **kwargs):
        context = super(StudentRegistration, self).get_context_data(**kwargs)
        context.update({'formset': self.formset})
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = self.formset_class()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        formset = self.formset_class(request.POST)
        if form.is_valid() and formset.is_valid():
            student = form.save()
            for form in formset:
                if form.has_changed():
                    guardian = form.save(commit=False)
                    guardian.student = student
                    guardian.save()
            return redirect("student-list")
        return render(request, self.template_name, {'form': form, 'formset': formset})


class StudentList(ListView):
    template_name = "student-list.html"
    queryset = Student.objects.all()
    context_object_name = "students"


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