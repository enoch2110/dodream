from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from website.models import Entry, EntryFile, EntryComment


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


admin.site.register(Entry, EntryAdmin)