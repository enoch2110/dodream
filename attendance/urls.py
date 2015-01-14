from django.conf.urls import patterns, url
from attendance.views import AttendanceList

urlpatterns = patterns('',
    url(r'^attendance-list', AttendanceList.as_view(), name="attendance-list"),
)
