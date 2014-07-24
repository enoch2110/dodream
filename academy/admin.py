from django.contrib import admin

# Register your models here.
from academy.models import *


class StudentModelAdmin(admin.ModelAdmin):
    search_fields = ('name', 'contact')


admin.site.register(Academy)
admin.site.register(Student, StudentModelAdmin)
admin.site.register(Staff)
admin.site.register(Guardian)
admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(Profile)