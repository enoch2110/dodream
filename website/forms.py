# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from academy.models import Profile
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


class UserCreateForm(UserCreationForm):
    contact = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ("last_name", "first_name", "username", "password1", "password2", "contact", "email")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user_profile = Profile(user=user, contact=self.cleaned_data['contact'])
        user_profile.save()
        return user, user_profile