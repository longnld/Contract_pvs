from rest_framework import serializers
from .models import Email_email
class Email_email_Serializer(serializers.ModelSerializer):
    class Meta():
        model=Email_email
        fields=['text_content','attachment_file'] 