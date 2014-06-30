from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('academy.views',
    (r'^$', TemplateView.as_view(template_name="index.html")),
    (r'^student-list$', TemplateView.as_view(template_name="student-list.html")),
    (r'^student-create$', TemplateView.as_view(template_name="student-list.html")),
)
