# -*- coding: utf-8 -*-
from django import forms
from multiupload.fields import MultiFileField
from website.models import *


# class PhotoAddForm(forms.ModelForm):
#     class Meta:
#         model = Photo
#
#
class EntryAddForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ['number', 'date']


class EntryCommentForm(forms.ModelForm):
    class Meta:
        model = EntryComment
        exclude = ['writer', 'entry', 'datetime']


class EntryAdminForm(forms.ModelForm):
    files = MultiFileField(max_num=10, min_num=0, max_file_size=1024*1024*5, required=False)

    class Meta:
        model = Entry

    def save(self, commit=True):
        super(EntryAdminForm, self).save(commit=commit)
        for file in self.cleaned_data['files']:
            entry_file = EntryFile(entry=self.instance, file=file)
            entry_file.save()
        return self.instance