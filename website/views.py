# -*- coding: utf8 -*-

from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, ListView, DetailView
from website.forms import EntryAddForm
from website.models import *


class EntryAdd(CreateView):
    template_name = "template_website/entry-add.html"
    model = Entry
    form_class = EntryAddForm

    def form_valid(self, form):
        return super(EntryAdd, self).form_valid(form)

    def get_success_url(self):
        return [self.get_object().type]+"-list.html"


class EntryList(ListView):
    model = Entry
    paginate_by = 9


    def get_queryset(self):
        return Entry.objects.filter(type=self.request.GET.get("type"))

    def get_template_names(self):
        return ["template_website/"+self.request.GET.get("type")+"-list.html"]


class EntryDetail(DetailView):
    model = Entry

    def get_template_names(self):
        return self.get_object().type+"-detail.html"