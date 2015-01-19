from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django_summernote.admin import SummernoteModelAdmin
from website.forms import UserCreateForm
from website.models import Entry, EntryFile, EntryComment, CarouselItem


class EntryFileInline(admin.StackedInline):
    model = EntryFile
    extra = 1


class EntryCommentInline(admin.StackedInline):
    model = EntryComment
    extra = 1


class EntryAdmin(SummernoteModelAdmin):
    list_display = ['type', 'title', 'datetime']
    list_filter = ['type']
    inlines = (EntryFileInline, EntryCommentInline)


class CarouselItemAdmin(SummernoteModelAdmin):
    list_display = ['title', 'subtitle', 'content', 'image']


class UserAdmin(UserAdmin):
    form = UserCreateForm
    add_fieldsets = ( (None, { 'classes': ('wide',), 'fields': ('username', 'password1', 'password2', )} ),)


admin.site.register(Entry, EntryAdmin)
admin.site.register(CarouselItem, CarouselItemAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
