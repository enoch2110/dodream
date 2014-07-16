from django.conf.urls import patterns, url
from api.views import Login, StudentListAPI, AttendanceCreateAPI

urlpatterns = patterns('',
    url(r'^login$', Login.as_view()),
    url(r'^students', StudentListAPI.as_view()),
    url(r'^attendance-create', AttendanceCreateAPI.as_view()),
    #url(r'^card-register', CardRegisterAPI.as_view())
)
