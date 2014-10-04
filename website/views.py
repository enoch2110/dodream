# -*- coding: utf8 -*-

from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, ListView, DetailView
from website.forms import PhotoAddForm, NoticeAddForm
from website.models import *


class PhotoAdd(CreateView):
    template_name = "template_website/gallery-photo-add.html"
    form_class = PhotoAddForm
    model = Photo
    success_url = "/photo-gallery"


class NoticeAdd(CreateView):
    template_name = "template_website/notice-add.html"
    model = Notice
    form_class = NoticeAddForm
    success_url = "/website/notice-list"

    def form_valid(self, form):
        return super(NoticeAdd, self).form_valid(form)


class NoticeList(ListView):
    template_name = "template_website/notice-list.html"
    context_object_name = "notices"
    queryset = Notice.objects.all()
    paginate_by = 10


class NoticeDetail(DetailView):
    template_name = "template_website/notice-detail.html"
    context_object_name = "notice"
    model = Notice
