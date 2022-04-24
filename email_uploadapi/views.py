from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from.models import Email_email,UploadFile
from .serializers import Email_email_Serializer
from rest_framework.decorators import api_view
# Create your views here.   
@api_view(['POST'])
def create_data(request):
    Subject= request.data['Subject']
    data_email = Email_email.objects.create(Subject=Subject)
    for f in request.data.getlist('Attachments'):
        file = UploadFile.objects.create(file=f)
        data_email.Attachments.add(file)
    data_email.save()
    
    serializer = Email_email_Serializer(data_email)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)
def getlist_Data(request):
    list_data=Email_email.objects.all().order_by("-id")
    return render(request,'email_uploadapi/list_data.html',{"list_data":list_data})