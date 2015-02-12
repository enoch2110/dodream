# -*- coding: utf8 -*-

from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.views.generic.edit import ModelFormMixin
from rest_framework.filters import SearchFilter
# from academy.admin import StudentModelAdmin, PaymentModelAdmin, CourseModelAdmin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from academy.admin import StudentModelAdmin
from academy.filters import StudentFilter
from academy.forms import *
from academy.models import *
from dodream.coolsms import send_sms

from django.http import *
from django.template import RequestContext
import socket
import json


class AcademySetting(UpdateView):
    template_name = "academy/academy-setting.html"
    form_class = AcademyForm
    success_url = "/setting"

    def get_object(self, queryset=None):
        return Academy.objects.get(id=self.request.user.profile.staff.academy.id)


class AccountCreate(CreateView):
    template_name = "academy/account-add.html"
    form_class = UserCreationForm

    def get_success_url(self):
        class_type = self.kwargs['type']
        if class_type in ["0", "2"]:
            return reverse("student-list")
        if class_type == "1":
            return reverse("staff-list")
        else:
            return "/"

    def form_valid(self, form):
        class_type = self.kwargs['type']
        pk = self.kwargs['pk']

        exists_1 = class_type == "0" and Student.objects.filter(id=pk).exists()
        exists_2 = class_type == "1" and Staff.objects.filter(id=pk).exists()
        exists_3 = class_type == "2" and Guardian.objects.filter(id=pk).exists()

        if exists_1 or exists_2 or exists_3:
            instance = form.save()
            if class_type == "0":
                profile = Student.objects.get(id=pk).profile
            if class_type == "1":
                profile = Staff.objects.get(id=pk).profile
            if class_type == "2":
                profile = Guardian.objects.get(id=pk).profile

            profile.user = instance
            profile.save()
            return super(AccountCreate, self).form_valid(form)
        else:
            return super(AccountCreate, self).form_invalid(form)


class StudentRegistration(View):
    template_name = "academy/student-add.html"
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
            student.academy = request.user.profile.staff.academy
            student.save()
            for form in formset:
                if form.has_changed():
                    guardian = form.save(commit=False)
                    guardian.student = student
                    guardian.save()
            return redirect("student-list")
        return render(request, self.template_name, {'form': form, 'formset': formset},)


class StudentUpdate(View):
    template_name = 'academy/student-update.html'
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
    template_name = "academy/student-list.html"
    queryset = Student.objects.all()
    context_object_name = "students"
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super(StudentList, self).get_context_data(**kwargs)
        context.update({"filter_form": StudentFilterForm(self.request.GET)})
        return context

    def get_queryset(self):
        search_param = self.request.GET.get('search')
        attend_method_param = self.request.GET.get('attend_method')
        is_paid_param = self.request.GET.get('is_paid')
        course_param = self.request.GET.get('course')

        students = StudentModelAdmin(Student, None).get_search_results(self.request, self.queryset, search_param)[0]
        students = StudentFilter(self.request.GET, queryset=students)

        return students

    def listing(request):
        student_list = Student.objects.all();
        paginator = Paginator(student_list, 10)

        page = request.GET.get('page')
        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_page)

        return render_to_response('academy/student-list.html', {"students": students})


class StudentDetail(DetailView):
    template_name = "academy/student-detail.html"
    context_object_name = "student"
    model = Student


class StaffList(ListView):
    template_name = "academy/staff-list.html"
    context_object_name = "staffs"
    paginate_by = 10

    def get_queryset(self):
        return Staff.objects.filter(academy=self.request.user.profile.staff.academy)


class StaffDetail(DetailView):
    template_name = "academy/staff-detail.html"
    context_object_name = "staff"
    model = Staff


class StaffCreate(CreateView):
    template_name = "academy/staff-add.html"
    model = Staff
    form_class = StaffForm
    success_url = "/staff-list"

    def form_valid(self, form):
        form.instance.academy = self.request.user.profile.staff.academy
        return super(StaffCreate, self).form_valid(form)


class StaffUpdate(UpdateView):
    template_name = "academy/staff-update.html"
    model = Staff
    form_class = StaffForm
    success_url = "/staff-list"


class StaffDelete(DeleteView):
    template_name = "academy/staff-delete.html"
    model = Staff
    success_url = "/staff-list"


class CategoryCreate(CreateView):
    template_name = "academy/category-add.html"
    model = Category
    form_class = CategoryCreateForm
    success_url = "/subject-list"

    def form_valid(self, form):
        form.instance.academy = self.request.user.profile.staff.academy
        return super(CategoryCreate, self).form_valid(form)


def subject_fee(request):
    if request.POST.has_key('id_subject'):
        sub_id = request.POST['id_subject']
        response_dict = {}
        response_dict.update({'fee': Subject.objects.get(id=sub_id).price})
        return HttpResponse(json.dumps(response_dict), content_type='application/json')
    else:
        return render_to_response('academy/student-subject-list.html', context_instance=RequestContext(request))


class SubjectCreate(CreateView):
    template_name = "academy/subject-add.html"
    model = Subject
    form_class = SubjectForm
    success_url = "/subject-list"


class SubjectUpdate(UpdateView):
    template_name = "academy/subject-update.html"
    model = Subject
    form_class = SubjectForm
    success_url = "/subject-list"


class SubjectDelete(DeleteView):
    template_name = "academy/subject-delete.html"
    model = Subject
    form_class = SubjectForm
    success_url = "/subject-list"


class SubjectList(ListView):
    template_name = "academy/subject-list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(academy=self.request.user.profile.staff.academy)


class StudentSubjectList(ListView):
    template_name = "academy/student-subject-list.html"
    queryset = StudentSubject.objects.all()
    context_object_name = "ss"

    def get_context_data(self, **kwargs):
        context = super(StudentSubjectList, self).get_context_data(**kwargs)
        context.update({"students": Student.objects.all()})
        return context


class StudentSubjectDetail(ListView):
    template_name = "academy/student-subject-detail.html"
    context_object_name = "subjects"

    def get_queryset(self):
        return StudentSubject.objects.filter(student__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(StudentSubjectDetail, self).get_context_data(**kwargs)
        context.update({"student": Student.objects.get(id=self.kwargs['pk'])})
        return context


class StudentSubjectCreate(CreateView):
    template_name = "academy/student-subject-add.html"
    model = StudentSubject
    form_class = StudentSubjectForm
    success_url = "/student-subject-list"

    def get_context_data(self, **kwargs):
        context = super(StudentSubjectCreate, self).get_context_data(**kwargs)
        context.update({"student": Student.objects.get(id=self.kwargs['pk'])})
        return context

    def form_valid(self, form):
        form.instance.student = Student.objects.get(id=self.kwargs['pk'])
        return super(StudentSubjectCreate, self).form_valid(form)


class StudentSubjectUpdate(UpdateView):
    template_name = "academy/student-subject-update.html"
    model = StudentSubject
    form_class = StudentSubjectForm
    success_url = "/student-subject-list"


class StudentSubjectDelete(DeleteView):
    template_name = "academy/student-subject-delete.html"
    model = StudentSubject
    success_url = "/student-subject-list"


def textbook_save(request):
    if 'stu_id' in request.GET and 'textbook_name' in request.GET:
        stu_id = request.GET['stu_id']
        textbook = request.GET['textbook_name']
        student = Student.objects.get(id=stu_id)
        student.textbook = textbook
        student.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


########################################################################################################################
# class CourseCategoryList(ListView):
#     template_name = "academy/course-list.html"
#     context_object_name = "root_categories"
#
#     def get_queryset(self):
#         queryset = CourseCategory.objects.filter(parent=None)
#         return queryset
#
#
# class CourseCreate(CreateView):
#     template_name = "academy/course-add.html"
#     model = Course
#     form_class = CourseForm
#     success_url = "/course-list"
#
#     def form_valid(self, form):
#         form.instance.academy = self.request.user.profile.staff.academy
#         return super(CourseCreate, self).form_valid(form)
#
#
# class CourseCategoryCreate(CreateView):
#     template_name = "academy/course-category.html"
#     model = CourseCategory
#     success_url = "/course-category-list"
#
#     def get_context_data(self, **kwargs):
#         context = super(CourseCategoryCreate, self).get_context_data(**kwargs)
#         context.update({'root_categories': CourseCategory.objects.filter(parent=None)})
#         return context
#
#
# class CourseUpdate(UpdateView):
#     template_name = "academy/course-update.html"
#     model = Course
#     form_class = CourseForm
#     success_url = "/course-list"
#
#
# class CourseDelete(DeleteView):
#     template_name = "academy/course-delete.html"
#     model = Course
#     success_url = "/course-list"
#
#
# class LectureList(ListView):
#     template_name = "academy/lecture-list.html"
#     model = Course
#     #queryset = Lecture.objects.filter(Lecture__course_parent=None)
#     #context_object_name = "root_categories"
#     # queryset = Course.objects.all()
#     context_object_name = "courses"
#
#     def get_queryset(self):
#         import datetime
#         if self.request.GET.get('date'):
#             date_begin = datetime.datetime.strptime(self.request.GET.get('date').split(" - ")[0], "%Y-%m-%d")
#             date_end = datetime.datetime.strptime(self.request.GET.get('date').split(" - ")[1], "%Y-%m-%d")
#             print date_begin
#             print date_end
#             daterange = [datetime.datetime.combine(date_begin, datetime.time.min), datetime.datetime.combine(date_end, datetime.time.max)]
#             queryset = Course.objects.filter(academy=self.request.user.profile.staff.academy)
#         else:
#             queryset = Course.objects.filter(academy=self.request.user.profile.staff.academy)
#         if self.request.GET.get('order'):
#             if self.request.GET.get('order') == "Date":
#                 queryset = queryset.order_by('price')
#             if self.request.GET.get('order') == "Amount":
#                 queryset = queryset.order_by('name')
#
#         return CourseModelAdmin(Course, None).get_search_results(self.request, queryset, self.request.GET.get('q'))[0]
#
#
# class LectureCreate(CreateView):
#     template_name = "academy/lecture-add.html"
#     model = Lecture
#     form_class = LectureForm
#     success_url = "/lecture-list"
#
#     def get_form_kwargs(self):
#         kwarg = super(LectureCreate, self).get_form_kwargs()
#         kwarg.update({'academy': self.request.user.profile.staff.academy})
#         return kwarg
#
#     def form_valid(self, form):
#         lecture = form.save()
#         datetime_string = self.request.POST.get('datetime')
#         datetimes = datetime_string.split(" - ")
#
#         for (counter, datetime) in enumerate(datetimes):
#             date_string = datetime.split(" ")[0]
#             hour_string = datetime.split(" ")[1].split(":")[0]
#             minute_string = datetime.split(" ")[1].split(":")[1]
#
#             new_date_string = date_string.split("/")[2]+"-"+date_string.split("/")[0]+"-"+date_string.split("/")[1]
#             new_time_string = hour_string if datetime.split(" ")[2] == "AM" else str((int(hour_string)+12%24)) + ":" + minute_string
#
#             type = 0 if counter == 0 else 1
#
#             lecture_datetime = LectureDateTime(date=datetime.split(" ")[0], time=datetime.split(" ")[1], lecture=lecture, type=type)
#             lecture_datetime.save()
#
#         return super(LectureCreate, self).form_valid(form)
#
#
# class LectureUpdate(UpdateView):
#     template_name = "academy/lecture-apply.html"
#     model = Lecture
#     form_class = LectureRegistrationForm
#     success_url = "/lecture-list"
#
#     def form_valid(self, form):
#         lecture = form.instance
#         students = form.cleaned_data['students']
#         price = self.request.POST.get('lecture-price')
#         # datetime_string = self.request.POST.get('datetime')
#         # datetimes = datetime_string.split(" - ")
#         for student in students:
#             student_lecture, created = StudentLecture.objects.get_or_create(lecture=lecture, student=student)
#             student_lecture.fee = price
#             student_lecture.save()
#             # for (counter, datetime) in enumerate(datetimes):
#             #     student_lecture.date = datetime.split(" ")
#             #     student_lecture.save()
#
#         return super(ModelFormMixin, self).form_valid(form)
#
#
# class PaymentList(ListView):
#     template_name = "academy/payment-list.html"
#     context_object_name = "payments"
#
#     def get_queryset(self):
#         import datetime
#         if self.request.GET.get('date'):
#             date_begin = datetime.datetime.strptime(self.request.GET.get('date').split(" - ")[0], "%Y-%m-%d")
#             date_end = datetime.datetime.strptime(self.request.GET.get('date').split(" - ")[1], "%Y-%m-%d")
#             print date_begin
#             print date_end
#             daterange = [datetime.datetime.combine(date_begin, datetime.time.min), datetime.datetime.combine(date_end, datetime.time.max)]
#             queryset = Payment.objects.filter(datetime__range=daterange)
#         else:
#             queryset = Payment.objects.all()
#         if self.request.GET.get('order'):
#             if self.request.GET.get('order') == "date":
#                 queryset = queryset.order_by('datetime')
#             if self.request.GET.get('order') == "name":
#                 queryset = queryset.order_by('student__name')
#             if self.request.GET.get('order') == "amount":
#                 queryset = queryset.order_by('amount')
#
#         return PaymentModelAdmin(Payment, None).get_search_results(self.request, queryset, self.request.GET.get('q'))[0]
#
#
# class PaymentCreate(CreateView):
#     template_name = "academy/payment-add.html"
#     model = Payment
#     form_class = PaymentForm
#     success_url = "/payment-list"
#
#
# class PaymentUpdate(UpdateView):
#     template_name = "academy/payment-update.html"
#     model = Payment
#     form_class = PaymentForm
#     success_url = "/payment-list"
#
#
# class PaymentDelete(DeleteView):
#     template_name = "academy/payment-delete.html"
#     model = Payment
#     success_url = "/payment-list"
#
#
# class UnpaidList(ListView):
#     template_name = "academy/unpaid-list.html"
#     context_object_name = "unpaids"
#
#     def get_queryset(self):
#         import datetime
#         if self.request.GET.get('date'):
#             date_begin = datetime.datetime.strptime(self.request.GET.get('date').split(" - ")[0], "%Y-%m-%d")
#             date_end = datetime.datetime.strptime(self.request.GET.get('date').split(" - ")[1], "%Y-%m-%d")
#             daterange = [date_begin, date_end]
#             queryset = StudentLecture.objects.filter(student__academy=self.request.user.profile.staff.academy, date__range=daterange)
#         else:
#             queryset = StudentLecture.objects.filter(student__academy=self.request.user.profile.staff.academy)
#         if self.request.GET.get('order'):
#             if self.request.GET.get('order') == "Date":
#                 queryset = queryset.order_by('date')
#             if self.request.GET.get('order') == "Name":
#                 queryset = queryset.order_by('student__name')
#             # if self.request.GET.get('order') == "Amount":
#             #     queryset = queryset.order_by('fee')
#         unpaids = []
#         for element in queryset:
#             if not element.student.is_paid():
#                 earliest = StudentLecture.objects.filter(student=element.student).earliest('date')
#                 if element == earliest:
#                     unpaids.append(earliest)
#         return unpaids
#         #return PaymentModelAdmin(Payment, None).get_search_results(self.request, unpaids, self.request.GET.get('q'))[0]
#         #list라 불가능ㅠㅠ
#
#         return queryset
#
#
# class UnpaidDetail(DetailView):
#     template_name = "academy/unpaid-detail.html"
#     context_object_name = "unpaid_student"
#     model = Student
#
#
# class TextbookUpdate(UpdateView):
#     template_name = "academy/textbook-update.html"
#     model = Student
#     form_class = TextbookForm
#     success_url = "/textbook-update"
#     context_object_name = "students"
#
#     def get_queryset(self):
#         return Student.objects.filter(academy=self.request.user.profile.staff.academy)
#
#
# def sms(request):
#     message = "신대호는 바보"#request.GET.get('message').encode('utf-8', 'ignore')
#     to = request.GET.get('to').encode('ascii')
#     if message and to:
#         send_sms(message, to)
#         return HttpResponse('sms sent')
#     else:
#         return HttpResponse('sms could not be sent')