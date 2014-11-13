from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from academy.views import *
from dodream.helpers import decorated_includes
from website.views import EntryAdd, EntryList, EntryDetail

urlpatterns = patterns('website.views',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^academy-introduction$', TemplateView.as_view(template_name="academy-introduction.html"), name="academy-introduction"),
    url(r'^academy-facilities$', TemplateView.as_view(template_name="academy-facilities.html"), name="academy-facilities"),
    url(r'^headmaster-introduction$', TemplateView.as_view(template_name="headmaster-introduction.html"), name="headmaster-introduction"),
    url(r'^staff-introduction$', TemplateView.as_view(template_name="staff-introduction.html"), name="staff-introduction"),
    url(r'^staff-introduction$', TemplateView.as_view(template_name="staff-introduction.html"), name="staff-introduction"),
    url(r'^academy-directions$', TemplateView.as_view(template_name="academy-directions.html"), name="academy-directions"),
    url(r'^elementary-course$', TemplateView.as_view(template_name="elementary-course.html"), name="elementary-course"),
    url(r'^intermediate-course$', TemplateView.as_view(template_name="intermediate-course.html"), name="intermediate-course"),
    url(r'^advanced-course$', TemplateView.as_view(template_name="advanced-course.html"), name="advanced-course"),
    url(r'^entrance-course$', TemplateView.as_view(template_name="entrance-course.html"), name="entrance-course"),
    url(r'^adult-course$', TemplateView.as_view(template_name="adult-course.html"), name="adult-course"),
    url(r'^entry-list$', EntryList.as_view(), name="entry-list"),
    url(r'^entry-detail/(?P<pk>\d+)', EntryDetail.as_view(), name="entry-detail"),
    url(r'^entry-add$', EntryAdd.as_view(), name="notice-add"),
    url(r'^schedule', TemplateView.as_view(template_name="schedule.html"), name="schedule"),
    url(r'^communication', TemplateView.as_view(template_name="communication.html"), name="communication"),
    url(r'^QnA', TemplateView.as_view(template_name="QnA.html"), name="QnA"),
)

