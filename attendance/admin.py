from django.contrib import admin

# Register your models here.
from attendance.models import Attendance, AttendancePolicy

admin.site.register(Attendance)
admin.site.register(AttendancePolicy)