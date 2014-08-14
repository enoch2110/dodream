from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from academy.views import *
from dodream.helpers import decorated_includes

urlpatterns = patterns('website.views',
    url(r'^$', TemplateView.as_view(template_name="template_website/home.html")),
    url(r'^academy-introduction$', TemplateView.as_view(template_name="template_website/academy-introduction.html"),
        name="academy-introduction"),
    url(r'^academy-facilities$', TemplateView.as_view(template_name="template_website/academy-facilities.html"),
        name="academy-facilities"),
    url(r'^headmaster-introduction$', TemplateView.as_view(template_name="template_website/headmaster-introduction.html"),
        name="headmaster-introduction"),
    url(r'^staff-introduction$', TemplateView.as_view(template_name="template_website/staff-introduction.html"),
        name="staff-introduction"),
    url(r'^staff-introduction$', TemplateView.as_view(template_name="template_website/staff-introduction.html"),
        name="staff-introduction"),
    url(r'^academy-directions$', TemplateView.as_view(template_name="template_website/academy-directions.html"),
        name="academy-directions"),
    url(r'^elementary-course$', TemplateView.as_view(template_name="template_website/elementary-course.html"),
        name="elementary-course"),
    url(r'^intermediate-course$', TemplateView.as_view(template_name="template_website/intermediate-course.html"),
        name="intermediate-course"),
    url(r'^advanced-course$', TemplateView.as_view(template_name="template_website/advanced-course.html"),
        name="advanced-course"),
    url(r'^entrance-course$', TemplateView.as_view(template_name="template_website/entrance-course.html"),
        name="entrance-course"),
    url(r'^adult-course$', TemplateView.as_view(template_name="template_website/adult-course.html"),
        name="adult-course"),
    url(r'^photo-gallery', TemplateView.as_view(template_name="template_website/photo-gallery.html"),
        name="photo-gallery"),
    url(r'^video-gallery', TemplateView.as_view(template_name="template_website/video-gallery.html"),
        name="video-gallery"),
    url(r'^notices', TemplateView.as_view(template_name="template_website/notices.html"),
        name="notices"),
    url(r'^schedule', TemplateView.as_view(template_name="template_website/schedule.html"),
        name="schedule"),
    url(r'^communication', TemplateView.as_view(template_name="template_website/communication.html"),
        name="communication"),
    url(r'^QnA', TemplateView.as_view(template_name="template_website/QnA.html"), name="QnA"),
)

