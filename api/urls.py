from django.conf.urls import patterns, url
from api.views import Login, StudentListAPI

urlpatterns = patterns('',
    url(r'^login$', Login.as_view()),
    url(r'^students', StudentListAPI.as_view()),
)
