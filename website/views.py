# -*- coding: utf8 -*-
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, ListView
from website.forms import EntryAddForm, EntryCommentForm, UserCreateForm
from website.models import *


class EntryAdd(CreateView):
    template_name = "website/entry-add.html"
    model = Entry
    form_class = EntryAddForm

    def form_valid(self, form):
        return super(EntryAdd, self).form_valid(form)

    def get_success_url(self):
        return ["website/"+self.get_object().type]+"-list.html"


class EntryList(ListView):
    model = Entry
    paginate_by = 9

    def get_queryset(self):
        return Entry.objects.filter(type=self.request.GET.get("type"))

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
