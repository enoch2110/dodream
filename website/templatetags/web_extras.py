from django import template
register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
    try:
        return field.as_widget(attrs={"class":css})
    except:
        return field


@register.filter(name='addattr')
def addattr(field, attr_string):
    attrs = {}
    for attr in attr_string.split(" "):
        attrs.update({attr.split("=")[0]: attr.split("=")[1]})
    return field.as_widget(attrs=attrs)