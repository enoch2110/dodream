from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="site_extras/index.html")),
    url(r'^send-code$', views.SMSVerify.as_view()),
    url(r'^contact$', views.InquiryCreate.as_view(), name="contact"),
    url(r'^username-check', views.UsernameDuplicateCheck.as_view(), name="username-check"),
]
