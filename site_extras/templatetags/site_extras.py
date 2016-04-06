# -*- coding: utf-8 -*-
from django.core.files.images import ImageFile
from easy_thumbnails.files import get_thumbnailer
import os
import re
import random
from django import template
from django.template.defaultfilters import linebreaksbr, safe
from ..models.sitemodels import Setting

register = template.Library()


@register.simple_tag
def add_attr(field, **kwargs):
    attrs = {}
    field_str = unicode(field.as_widget())
    for arg in kwargs:
        if arg == "attr_str":
            attr_strs = kwargs[arg].split(" ")
            for attr in attr_strs:
                attr_str = attr.split("=")

                if len(attr_str) == 2:
                    attrs.update({attr_str[0]: attr_str[1]})
                elif len(attr_str) == 1:
                    attrs.update({attr_str[0]: ""})

        elif arg not in field_str:
            attrs.update({arg: kwargs[arg]})

    return field.as_widget(attrs=attrs)

@register.filter(name='call')
def call(obj, method_name):
    method = getattr(obj, method_name)

    if obj.__dict__.has_key("__callArg"):
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()

@register.filter(name='arg')
def args(obj, arg):
    if not obj.__dict__.has_key("__callArg"):
        obj.__callArg = []
    obj.__callArg += [arg]
    return obj


@register.filter(name='setting')
def setting(name, arg):
    setting, created = Setting.objects.get_or_create(name=name)
    if setting:
        if arg == "content":
            if setting.is_richtext:
                return safe(setting.content)
            else:
                return linebreaksbr(setting.content)
        elif arg == "files":
            return setting.files.all()
        elif arg == "file_url":
            if setting.files.first():
                return setting.files.first().file.url
            else:
                return None
        elif arg == "file":
            if setting.files.first():
                return setting.files.first().file
            else:
                return None
    return setting


@register.filter(name='is_old_ie')
def is_old_ie(request):
    is_ie = False

    if request.META.has_key('HTTP_USER_AGENT'):
        user_agent = request.META['HTTP_USER_AGENT']

        # Test IE 1-7
        pattern = "msie [1-8]\."
        prog = re.compile(pattern, re.IGNORECASE)
        match = prog.search(user_agent)

        if match:
            is_ie = True

    return is_ie


@register.filter(name='shuffle')
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp


@register.filter(name='get_image')
def get_image(arg):
    from django.conf import settings
    picture = open(os.path.join(settings.BASE_DIR, arg))
    thumbnailer = ImageFile(picture)
    return thumbnailer


@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()


@register.filter('widget')
def widget(field):
    return field.field.widget.__class__.__name__


@register.inclusion_tag('site_extras/form/fieldset.html')
def fieldset(fieldset, **kwargs):
    context = kwargs
    context['fieldset'] = fieldset
    return context


@register.inclusion_tag('site_extras/form/field.html')
def field(field, **kwargs):
    context = kwargs
    context['field'] = field
    return context