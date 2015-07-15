# -*- coding: utf8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured

from django.shortcuts import render
from django.shortcuts import redirect, render_to_response

# Create your views here.
from django.views.generic import *
from website.forms import *
from website.models import *
from academy.models import Student
from academy.forms import StudentCommentForm
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.staticfiles.templatetags.staticfiles import static


class EntryAdd(CreateView):
    template_name = "academy/entry-add.html"
    model = Entry
    form_class = EntryAddForm

    def get_success_url(self):
        return "entry-detail/" + str(self.object.pk)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.writer = self.request.user
        instance.save()
        for item in form.cleaned_data['files']:
            EntryFile.objects.create(file=item, entry=instance)
        return super(EntryAdd, self).form_valid(form)


class EntryList(ListView):
    model = Entry
    paginate_by = 18

    def get_queryset(self):
        return Entry.objects.filter(type=self.request.GET.get("type")).order_by('-datetime')

    def get_template_names(self):
        return ["website/"+self.request.GET.get("type")+"-list.html"]


class EntryDetail(CreateView):
    model = EntryComment
    form_class = EntryCommentForm

    def get_context_data(self, **kwargs):
        context = super(EntryDetail, self).get_context_data(**kwargs)
        post_id = self.kwargs['pk']
        try:
            context['object'] = Entry.objects.get(id=post_id)
            context['files'] = EntryFile.objects.filter(entry=post_id)
        except:
            pass
        return context

    def form_valid(self, form):
        form.instance.writer = self.request.user
        form.instance.entry = self.get_context_data()['object']
        return super(EntryDetail, self).form_valid(form)

    def get_template_names(self):
        post_id = self.kwargs['pk']
        try:
            object = Entry.objects.get(id=post_id)
        except:
            pass
        return "website/"+object.type+"-detail.html"

    def get_success_url(self):
        return self.request.path


class CarouselItemView(ListView):
    model = CarouselItem
    template_name = "website/index.html"
    context_object_name = "carousel_items"

    def get_queryset(self):
        return CarouselItem.objects.all()


class UserCreateView(CreateView):
    template_name = "website/join.html"
    model = User
    form_class = UserCreateForm
    success_url = "/website"


class WebsiteStudentList(ListView):
    template_name = "website/student-list.html"
    # queryset = Student.objects.all().order_by('name')
    # paginate_by = 18

    def get_context_data(self, **kwargs):
        context = super(WebsiteStudentList, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated():
            context['mes'] = '로그인이 필요합니다'
        return context

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated():
            return Student.objects.none()
        if user.is_staff or user.is_superuser:
            return Student.objects.all().order_by('name')
        elif Guardian.objects.filter(profile__user=user).exists():
            print('guardian exists')
            students = set()
            for guardian in Guardian.objects.filter(profile__user=user):
                students.add(guardian.student.id)
            # guardian = Guardian.objects.get(profile__user=user)
            return Student.objects.filter(id__in=students)


class WebsiteStudentDetail(CreateView):
    template_name = "website/student-detail.html"
    form_class = StudentCommentForm

    def get_context_data(self, **kwargs):
        context = super(WebsiteStudentDetail, self).get_context_data(**kwargs)
        post_id = self.kwargs['pk']
        try:
            context['object'] = Student.objects.get(id=post_id)
        except:
            pass
        return context