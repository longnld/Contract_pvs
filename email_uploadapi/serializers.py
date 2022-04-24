from rest_framework import serializers
from .models import Email_email,UploadFile
class UploadSerializers(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ('file',)

class Email_email_Serializer(serializers.ModelSerializer):
    Attachments = UploadSerializers(many=True, read_only=True)
    class Meta():
        model=Email_email
        fields=("Subject","Attachments")