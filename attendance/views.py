from django.views.generic import ListView
from attendance.models import Attendance


class AttendanceList(ListView):
    model = Attendance
    template_name = "academy/attendance-list.html"
    context_object_name = "attendances"