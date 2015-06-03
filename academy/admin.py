from django import forms
from django.conf import settings
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from academy.forms import StaffForm
from academy.models import *
from attendance.models import AttendanceManager

admin.site.unregister(User)

class AttendanceManagerInline(admin.StackedInline):
    model = AttendanceManager


class UserProfileInline(admin.StackedInline):
    model = Profile


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]


class GuardianInline(admin.TabularInline):
    model = Guardian
    extra = 0


class StudentModelAdmin(admin.ModelAdmin):
    search_fields = ('name', 'contact')
    inlines = (GuardianInline, )
    list_display = ['name', 'birthday', 'registered_date', 'gender', 'use_sms', 'contact']

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "user":
            kwargs['queryset'] = User.objects.filter(student=None, staff=None)
        return super(StudentModelAdmin, self).formfield_for_foreignkey(db_field, request=None, **kwargs)


class StaffAdmin(admin.ModelAdmin):
    exclude = ['profile']
    form = StaffForm


# class PaymentModelAdmin(admin.ModelAdmin):
#     search_fields = ['student__name']
#
#
# class CourseModelAdmin(admin.ModelAdmin):
#     search_fields = ['name']
#
#
# class LectureDateTimeInline(admin.TabularInline):
#     model = LectureDateTime
#     extra = 0
#
#
# class LectureAdmin(admin.ModelAdmin):
#     inlines = [LectureDateTimeInline]


class SettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'academy']


admin.site.register(Profile)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Academy)
admin.site.register(Student, StudentModelAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Category)
admin.site.register(Subject)
admin.site.register(StudentSubject)
# admin.site.register(Course)
# admin.site.register(CourseCategory)
# admin.site.register(Payment)
# admin.site.register(Lecture, LectureAdmin)
# admin.site.register(StudentLecture)
# admin.site.register(LectureDateTime)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Guardian)
admin.site.register(StudentMemo)