from django.contrib import admin

# Register your models here.
from attendance.models import Attendance, AttendancePolicy, AttendanceManager

admin.site.register(Attendance)
admin.site.register(AttendancePolicy)
admin.site.register(AttendanceManager)