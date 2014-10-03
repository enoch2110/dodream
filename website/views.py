# -*- coding: utf8 -*-

from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from website.forms import PhotoAddForm
from website.models import *


class PhotoAdd(CreateView):
    template_name = "template_website/gallery-photo-add.html"
    form_class = PhotoAddForm
    model = Photo
    success_url = "/photo-gallery"