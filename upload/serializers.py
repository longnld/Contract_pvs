from rest_framework import serializers
from .models import file
class FileSerializers(serializers.ModelSerializer):
    class Meta:
        model = file
        fields = ('file',)
