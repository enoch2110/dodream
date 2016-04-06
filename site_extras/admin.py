# -*- coding: utf-8 -*-

from django.contrib import admin
from site_extras.forms import SettingForm
from site_extras.models.sitemodels import Setting, SettingFile, Inquiry
from site_extras.models.utilmodels import SMSVerification


class SMSVerificationAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'phone_number', 'code', 'is_verified']

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser


class SettingFileInline(admin.TabularInline):
    model = SettingFile
    extra = 0


class SettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'help_text', 'get_partial_content']
    list_filter = ['type']
    ordering = ['type', 'name']
    inlines = [SettingFileInline]
    form = SettingForm

    def get_partial_content(self, obj):
        return (obj.content[:75] + '..') if len(obj.content) > 75 else obj.content

    get_partial_content.short_description = u"내용"

    def has_delete_permission(self, request, obj=None):
        return self.has_conf_permission(request)

    def has_add_permission(self, request):
        return self.has_conf_permission(request)

    def get_readonly_fields(self, request, obj=None):
        return ['type', 'name', 'help_text', 'is_richtext'] if obj and not self.has_conf_permission(request) else []

    def has_conf_permission(self, request):
        return request.user.is_superuser and request.user.username == "superuser"

    class Meta:
        labels = {
            'name': "제목"
        }


class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'email', 'title']


class PopupAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_begin', 'date_end', 'is_active']

admin.site.register(Setting, SettingAdmin)
