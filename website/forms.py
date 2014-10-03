# -*- coding: utf-8 -*-
from django import forms
from website.models import *


class PhotoAddForm(forms.ModelForm):
    class Meta:
        model = Photo