from django.db import models

# Create your models here.
class Email_email(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    text_content=models.TextField()
    attachment_file=models.FileField(blank=True,null=True)
    