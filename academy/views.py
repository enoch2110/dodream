from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.views.generic.edit import ModelFormMixin
from rest_framework.filters import SearchFilter
from academy.admin import StudentModelAdmin
from academy.forms import *
from academy.models import *


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

    def form_valid(self, form):
        form.instance.academy = self.request.user.profile.staff.academy
        return super(CourseCreate, self).form_valid(form)


class CourseCategoryCreate(CreateView):
    template_name = "course-category.html"
    model = CourseCategory
    success_url = "/course-category-list"

    def get_context_data(self, **kwargs):
        context = super(CourseCategoryCreate, self).get_context_data(**kwargs)
        context.update({'root_categories': CourseCategory.objects.filter(parent=None)})
        return context


class LectureList(ListView):
    template_name = "lecture-list.html"
    model = Course
    #queryset = Lecture.objects.filter(Lecture__course_parent=None)
    #context_object_name = "root_categories"
    queryset = Course.objects.all()
    context_object_name = "courses"


class LectureCreate(CreateView):
    template_name = "lecture-add.html"
    model = Lecture
    form_class = LectureForm
    success_url = "/lecture-list"

    def form_valid(self, form):
        lecture = form.save()
        datetime_string = self.request.POST.get('datetime')
        datetimes = datetime_string.split(" - ")

        for (counter, datetime) in enumerate(datetimes):
            date_string = datetime.split(" ")[0]
            hour_string = datetime.split(" ")[1].split(":")[0]
            minute_string = datetime.split(" ")[1].split(":")[1]

            new_date_string = date_string.split("/")[2]+"-"+date_string.split("/")[0]+"-"+date_string.split("/")[1]
            new_time_string = hour_string if datetime.split(" ")[2] == "AM" else str((int(hour_string)+12%24)) + ":" + minute_string

            type = 0 if counter == 0 else 1

            lecture_datetime = LectureDateTime(date=new_date_string, time=new_time_string, lecture=lecture, type=type)
            lecture_datetime.save()

        return super(LectureCreate, self).form_valid(form)


class LectureUpdate(UpdateView):
    template_name = "lecture-apply.html"
    model = Lecture
    form_class = LectureRegistrationForm
    success_url = "/lecture-list"

    def form_valid(self, form):
        lecture = form.instance
        students = form.cleaned_data['students']
        price = self.request.POST.get('lecture-price')
        datetime_string = self.request.POST.get('datetime')
        datetimes = datetime_string.split(" - ")
        for student in students:
            student_lecture, created = StudentLecture.objects.get_or_create(lecture=lecture, student=student)
            print "why"
            student_lecture.fee = price
            for (counter, datetime) in enumerate(datetimes):
                date_string = datetime.split(" ")[0]
                hour_string = datetime.split(" ")[1].split(":")[0]
                minute_string = datetime.split(" ")[1].split(":")[1]

                new_date_string = date_string.split("/")[2]+"-"+date_string.split("/")[0]+"-"+date_string.split("/")[1]
                new_time_string = hour_string if datetime.split(" ")[2] == "AM" else str((int(hour_string)+12%24)) + ":" + minute_string

                student_lecture.date = new_date_string
                student_lecture.save()

        return super(ModelFormMixin, self).form_valid(form)