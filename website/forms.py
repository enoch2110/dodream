# -*- coding: utf-8 -*-
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from academy.models import Profile, Guardian
from multiupload.fields import MultiFileField
from website.models import *


class EntryAddForm(forms.ModelForm):
    files = MultiFileField(max_num=10, min_num=0, max_file_size=1024*1024*5, required=False)

    class Meta:
        model = Entry
        fields = ['type', 'title', 'subtitle', 'files', 'content']

    def clean(self):
        cleaned_data = super(EntryAddForm, self).clean()
        type = cleaned_data.get("type")
        files = cleaned_data.get("files")
        if type == 'gallery' and not files:
            self.add_error('files', "이 항목을 채워주십시오.")

        return cleaned_data



class EntryCommentForm(forms.ModelForm):
    class Meta:
        model = EntryComment
        fields = '__all__'
        exclude = ['writer', 'entry', 'datetime']


class EntryAdminForm(forms.ModelForm):
    writer = forms.ModelChoiceField(queryset=User.objects.filter(profile__staff__isnull=False))
    files = MultiFileField(max_num=10, min_num=0, max_file_size=1024*1024*5, required=False)

    class Meta:
        model = Entry
        fields = '__all__'

    def save(self, commit=True):
        super(EntryAdminForm, self).save(commit=commit)
        for file in self.cleaned_data['files']:
            entry_file = EntryFile(entry=self.instance, file=file)
            entry_file.save()
        return self.instance


class UserCreateForm(UserCreationForm):
    contact = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ("last_name", "first_name", "username", "password1", "password2", "contact", "email")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.save()
        contact = self.cleaned_data['contact']
        if Guardian.objects.filter(contact=contact).exists():
            for guardian in Guardian.objects.filter(contact=contact):
                guardian.email = self.cleaned_data["email"]
                profile = guardian.profile.id
                if Profile.objects.filter(id=profile).exists():
                    Profile.objects.filter(id=profile).delete()
                Profile.objects.filter(id=profile).update(user=user)
        else:
            user_profile = Profile(user=user)
            user_profile.save()
        return user
