from __future__ import unicode_literals
from django.db import models
import os
def validate_file_extension1(value):
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[-1]  # [0] returns path+filename
    valid_extensions = ['.pdf',]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents',validators=[validate_file_extension1])



