from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from academy.views import *
from dodream.helpers import decorated_includes

urlpatterns = patterns('website.views',
    url(r'^$', TemplateView.as_view(template_name="template_website/home.html")),
    # url(r'^setting$', AcademySetting.as_view(), name="academy-setting"),
)
    
