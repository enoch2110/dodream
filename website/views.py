# -*- coding: utf8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured

from django.shortcuts import render
from django.shortcuts import redirect, render_to_response

# Create your views here.
from django.views.generic import CreateView, ListView
from website.forms import *
from website.models import *
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.staticfiles.templatetags.staticfiles import static


class EntryAdd(CreateView):
    template_name = "academy/entry-add.html"
    model = Entry
    form_class = EntryAddForm
    file_class = EntryFileForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        files = self.file_class()
        return render(request, self.template_name, {'form': form, 'files': files})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        files = self.file_class(request.POST, request.FILES)
        if form.is_valid() and files.is_valid():
            entry = form.save(commit=False)
            entry.writer = self.request.user
            entry.save()
            for item in files.cleaned_data['files']:
                obj = EntryFile(file=item, entry=entry)
                obj.save()
            return redirect("entry-detail/" + str(entry.id))
        return render_to_response(self.template_name, {'form': form, 'files': files}, context_instance=RequestContext(request))

    def form_valid(self, form):
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
