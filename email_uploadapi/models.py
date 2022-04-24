from django.db import models

# Create your models here.

class UploadFile(models.Model):
	file = models.FileField()
	def __str__(self):
		return "{}".format(self.file)
	
class Email_email(models.Model):
	created=models.DateTimeField(auto_now_add=True)
	Subject=models.TextField()
	Attachments=models.ManyToManyField(UploadFile,blank=True) 