from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from academy.views import StudentRegistration

urlpatterns = patterns('academy.views',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^student-list$', TemplateView.as_view(template_name="student-list.html")),
    url(r'^student-create$', StudentRegistration.as_view(), name="student-registration"),
)
