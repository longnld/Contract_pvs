from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import Email_email_Serializer
# Create your views here.
class Email_email_View(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self,request,*args,**kwargs):
        file_serializer=Email_email_Serializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)