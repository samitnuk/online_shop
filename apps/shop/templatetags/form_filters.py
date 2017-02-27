from django import template
from django.forms import CheckboxInput, HiddenInput


register = template.Library()


@register.filter
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == \
        CheckboxInput().__class__.__name__


@register.filter
def is_hidden(field):
    return field.field.widget.__class__.__name__ == \
        HiddenInput().__class__.__name__
