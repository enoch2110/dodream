# -*- coding: utf8 -*-

from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from rest_framework.filters import SearchFilter
from academy.admin import StudentModelAdmin, PaymentModelAdmin
from academy.forms import *
from academy.models import *
from dodream.coolsms import send_sms


class AcademySetting(UpdateView):
    template_name = "academy-setting.html"
    form_class = AcademyForm
    success_url = "/setting"

    def get_object(self, queryset=None):
        return Academy.objects.get(id=self.request.user.staff.academy.id)


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


class CourseUpdate(UpdateView):
    template_name = "course-update.html"
    model = Course
    form_class = CourseForm
    success_url = "/course-list"


class CourseDelete(DeleteView):
    template_name = "course-delete.html"
    model = Course
    success_url = "/course-list"


class LectureList(ListView):
    template_name = "lecture-list.html"
    model = Lecture
    #queryset = Lecture.objects.filter(Lecture__course_parent=None)
    #context_object_name = "root_categories"
    queryset = Lecture.objects.all()
    context_object_name = "lectures"


class LectureCreate(CreateView):
    template_name = "lecture-add.html"
    model = Lecture
    form_class = LectureForm
    success_url = "/lecture-list"


class PaymentList(ListView):
    template_name = "payment-list.html"
    context_object_name = "payments"

    def get_queryset(self):
        import datetime
        if self.request.GET.get('date'):
            date_begin = datetime.datetime.strptime(self.request.GET.get('date').split(" - ")[0], "%Y-%m-%d")
            date_end = datetime.datetime.strptime(self.request.GET.get('date').split(" - ")[1], "%Y-%m-%d")
            print date_begin
            print date_end
            daterange = [datetime.datetime.combine(date_begin, datetime.time.min), datetime.datetime.combine(date_end, datetime.time.max)]
            queryset = Payment.objects.filter(datetime__range=daterange)
        else:
            queryset = Payment.objects.all()


        return PaymentModelAdmin(Payment, None).get_search_results(self.request, queryset, self.request.GET.get('q'))[0]


class PaymentCreate(CreateView):
    template_name = "payment-add.html"
    model = Payment
    form_class = PaymentForm
    success_url = "/payment-list"


class PaymentDelete(DeleteView):
    template_name = "payment-delete.html"
    model = Payment
    success_url = "/payment-list"


def sms(request):
    message = "신대호는 바보"#request.GET.get('message').encode('utf-8', 'ignore')
    to = request.GET.get('to').encode('ascii')
    if message and to:
        send_sms(message, to)
        return HttpResponse('sms sent')
    else:
        return HttpResponse('sms could not be sent')