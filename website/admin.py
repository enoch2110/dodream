from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
# from academy.models import Profile
from django.db import models
from django import forms
# from website.forms import EntryAdminForm
from website.models import Entry, EntryFile, EntryComment, CarouselItem


class EntryFileInline(admin.StackedInline):
    model = EntryFile
    extra = 1


class EntryCommentInline(admin.StackedInline):
    model = EntryComment
    extra = 1


class EntryAdmin(admin.ModelAdmin):
    # formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }
    list_display = ['type', 'title', 'datetime']
    list_filter = ['type']
    # form = EntryAdminForm
    inlines = (EntryFileInline, EntryCommentInline,)

    # class Media:
    #     js = ('ckeditor/ckeditor.js',)


class CarouselItemAdmin(SummernoteModelAdmin):
    list_display = ['title', 'subtitle', 'content', 'image']


# class UserAdmin(UserAdmin):
#     form = UserCreateForm
#     add_fieldsets = ( (None, { 'classes': ('wide',), 'fields': ('username', 'password1', 'password2', )} ),)


admin.site.register(Entry, EntryAdmin)
admin.site.register(CarouselItem, CarouselItemAdmin)
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
