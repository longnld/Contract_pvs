from django import template
import os
register =template.Library()

@register.filter(name="extensiontags")
def extensiontags(value,*args):
    slices=str(value).split(".")
    return slices[1]
