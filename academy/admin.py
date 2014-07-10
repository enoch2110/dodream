from django.contrib import admin

# Register your models here.
from academy.models import *

admin.site.register(Academy)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Guardian)
admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(Profile)