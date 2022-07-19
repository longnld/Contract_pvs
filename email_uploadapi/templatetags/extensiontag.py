from django import template
import os
register =template.Library()

@register.filter(name="extensiontags")
def extensiontags(value,*args):
    if value.endswith(".pdf"):
        return "pdf"
