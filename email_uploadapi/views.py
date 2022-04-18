from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import Email_email_Serializer
# Create your views here.   
def modify_input_for_multiple_files(Subject, Attachments):
    dict = {}
    dict['Subject'] = Subject
    dict['Attachments'] = Attachments
    return dict
class Email_email_View(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self,request,*args,**kwargs):
        Subject = request.data.get('Subject')
        Attachments = dict((request.data).lists())['Attachments']
        flag = 1
        arr = []
        for attachment in Attachments:
            modified_data = modify_input_for_multiple_files( Subject, attachment)
            file_serializer = Email_email_Serializer(data=modified_data)

            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)