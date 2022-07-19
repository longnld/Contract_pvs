from django import template
import os
register =template.Library()

@register.filter(name="extensiontags")
def extensiontags(value,*args):
    value=str(value)
    if value.endswith(".pdf"):
        return "pdf"
