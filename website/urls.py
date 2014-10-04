from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from academy.views import *
from dodream.helpers import decorated_includes
from website.views import PhotoAdd, NoticeAdd, NoticeList, NoticeDetail

urlpatterns = patterns('website.views',
    url(r'^$', TemplateView.as_view(template_name="template_website/index.html")),
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
    url(r'^photo-gallery', TemplateView.as_view(template_name="template_website/gallery-photo.html"),
        name="photo-gallery"),
    url(r'^photo-add', PhotoAdd.as_view(), name="photo-add"),
    url(r'^video-gallery', TemplateView.as_view(template_name="template_website/gallery-video.html"),
        name="video-gallery"),
    url(r'^notice-list$', NoticeList.as_view(), name="notice-list"),
    url(r'^notice-add$', NoticeAdd.as_view(), name="notice-add"),
    url(r'^notice-detail/(?P<pk>\d+)$', NoticeDetail.as_view(), name="notice-detail"),
    url(r'^schedule', TemplateView.as_view(template_name="template_website/schedule.html"),
        name="schedule"),
    url(r'^communication', TemplateView.as_view(template_name="template_website/communication.html"),
        name="communication"),
    url(r'^QnA', TemplateView.as_view(template_name="template_website/QnA.html"), name="QnA"),
    # url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'template_website/login.html'},name="login"),
    # url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'template_website/logout.html'}, name="logout"),
)

