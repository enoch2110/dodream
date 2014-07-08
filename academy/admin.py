from django.contrib import admin

# Register your models here.
from academy.models import Student, Guardian, CourseCategory, Course

admin.site.register(Student)
admin.site.register(Guardian)
admin.site.register(Course)
admin.site.register(CourseCategory)