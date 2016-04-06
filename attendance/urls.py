from django.conf.urls import url
from attendance.views import AttendanceList

urlpatterns = [
    url(r'^attendance-list', AttendanceList.as_view(), name="attendance-list"),
]