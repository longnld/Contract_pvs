from django.db import models

# Create your models here.
class Email_email(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    Subject=models.TextField()
    Attachments=models.FileField(blank=True,null=True)
    