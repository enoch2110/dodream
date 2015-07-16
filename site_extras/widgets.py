# -*- coding: utf-8 -*-

from django import forms
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.html import format_html


class DisablePopulatedText(forms.TextInput):
    def __init__(self, obj, attrs=None):
        self.object = obj
        super(DisablePopulatedText, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        # if value is None:
        #     value = ''
        # final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        # if value != '':
        #     # Only add the 'value' attribute if a value is non-empty.
        #     final_attrs['value'] = force_text(self._format_value(value))
        # if "__prefix__" not in name and not value:
        #     return format_html('<input{0} disabled />', flatatt(final_attrs))
        # else:
        #     return format_html('<input{0} />', flatatt(final_attrs))
        return format_html("fuckyou")

class SMSValidateWidget(forms.MultiWidget):

    def __init__(self, *args, **kwargs):
        subfield_1_attrs = kwargs.pop("subfield_1_attrs")
        subfield_2_attrs = kwargs.pop("subfield_2_attrs")

        widgets = [
            forms.TextInput(attrs=subfield_1_attrs),
            forms.TextInput(attrs=subfield_2_attrs)
        ]
        super(SMSValidateWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        return [None, None]

    def format_output(self, rendered_widgets):
        widget_context = {'phone_number': rendered_widgets[0], 'code': rendered_widgets[1]}
        return render_to_string('site_extras/forms/smsvalidatefield.html', widget_context)