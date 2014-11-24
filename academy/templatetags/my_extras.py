from django import template
register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
    try:
        return field.as_widget(attrs={"class":css})
    except:
        return field


@register.inclusion_tag('academy/_includes/_children.html')
def children_tag(parent):
    children = parent.children()
    return {'children': children}


@register.inclusion_tag('academy/_includes/_child_categories.html')
def child_categories(parent):
    children = parent.children()
    return {'children': children}

@register.filter(name='addattr')
def addattr(field, attr_string):
    attrs = {}
    for attr in attr_string.split(" "):
        attrs.update({attr.split("=")[0]: attr.split("=")[1]})
    return field.as_widget(attrs=attrs)