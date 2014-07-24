from django import forms
from django.conf import settings
from django.contrib import admin

# Register your models here.
from academy.forms import StaffForm
from academy.models import *


class StudentModelAdmin(admin.ModelAdmin):
    search_fields = ('name', 'contact')

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "user":
            kwargs['queryset'] = User.objects.filter(student=None, staff=None)
        return super(StudentModelAdmin, self).formfield_for_foreignkey(db_field, request=None, **kwargs)


class StaffAdmin(admin.ModelAdmin):
    form = StaffForm
    exclude = ['user']


class PaymentModelAdmin(admin.ModelAdmin):
    search_fields = ['student__name']


admin.site.register(Academy)
admin.site.register(Student, StudentModelAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Guardian)
admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(Profile)
admin.site.register(Payment)
admin.site.register(Lecture)
