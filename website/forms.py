# -*- coding: utf-8 -*-
from django import forms
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