from email.policy import default
from pyexpat import model
from django.db import models
from django.urls import reverse
# Create your models here.

class UploadFile(models.Model):
	file = models.FileField()
	def __str__(self):
		return "{}".format(self.file)
	
class Email_email(models.Model):
	CHOICES = [
    ('OPEN', 'open'),
    ('PROCESSING', 'processing'),
    ('PENDING', 'pending'),
    ('CLOSE', 'close'),
]
	sender=models.EmailField(max_length = 254,null=True)
	created=models.DateTimeField(null=True,blank=True)
	Subject=models.TextField()
	Attachments=models.ManyToManyField(UploadFile,blank=True) 
	note=models.TextField(null=True,blank=True)
	date_to_close=models.DateTimeField(null=True,blank=True)
	status=models.CharField( max_length=20,choices=CHOICES,default="open")
	def __str__(self):
		return "{}".format(self.Subject)
	
	def get_email_delete_url(self):
		return reverse("email_api:email_delete",kwargs={"pk":self.pk})

