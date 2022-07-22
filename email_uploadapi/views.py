
from urllib import response
from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from.models import Email_email,UploadFile
from .serializers import Email_email_Serializer
from rest_framework.decorators import api_view
from datetime import datetime
from datetime import timedelta
from django.db.models import Q
from.forms import EmailFormUpdate
# Create your views here.

  
@api_view(['POST'])
def create_data(request):
    replyFilter=["RE","Re","Trả lời"]
    fwFilter =["FW","fw","Fwd"]
    subject= request.data['Subject']
    subjectText=subject.replace(":","",1)
    if request.data['sender'] == "sales.promotion@kcc.com":
        return Response("sales.promotion@kcc.com", status=status.HTTP_201_CREATED)
    elif request.data['sender'].endswith("kcc.com"):
        if any(word in subjectText for word in replyFilter ):
            for word in replyFilter:
                subjectWithoutReplyIndex=subjectText.find(word)
                if subjectWithoutReplyIndex!= -1:
                    subjectWithoutReply=subjectText.replace(word,"").strip() 
                    subjectFw=subjectText.replace(word,"FW:").strip()
            dataEmail=Email_email.objects.all().filter(Q(Subject__icontains=subjectWithoutReply,created__gte=datetime.now()-timedelta(days=2)))
            if dataEmail.count() != 0:
                dataEmail=dataEmail.first()
                for f in request.data.getlist('Attachments'):
                    file = UploadFile.objects.create(file=f)
                    dataEmail.Attachments.add(file)
                if dataEmail.sender != request.data['sender']:
                    try:
                        dataEmail.note= dataEmail.note + request.data['sender']
                    except:
                        dataEmail.note=request.data['sender']               
                dataEmail.save()
                serializer = Email_email_Serializer(dataEmail)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                dataEmail = Email_email.objects.create(Subject=subjectFw)
                for f in request.data.getlist('Attachments'):
                    file = UploadFile.objects.create(file=f)
                    dataEmail.Attachments.add(file)
                dataEmail.sender=request.data['sender']
                dataEmail.created=datetime.now()
                dataEmail.save()
                serializer = Email_email_Serializer(dataEmail)       
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif any(word in subjectText for word in fwFilter ):
                subjectFw=subjectText.replace(word,"FW:").strip()
                dataEmail = Email_email.objects.create(Subject=subjectFw)
                for f in request.data.getlist('Attachments'):
                    file = UploadFile.objects.create(file=f)
                    dataEmail.Attachments.add(file)
                dataEmail.sender=request.data['sender']
                dataEmail.created=datetime.now()
                dataEmail.save()
                serializer = Email_email_Serializer(dataEmail)       
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            dataEmail = Email_email.objects.create(Subject=subject)
            for f in request.data.getlist('Attachments'):
                file = UploadFile.objects.create(file=f)
                dataEmail.Attachments.add(file)
            dataEmail.sender=request.data['sender']
            dataEmail.created=datetime.now()
            dataEmail.save()
            serializer = Email_email_Serializer(dataEmail)       
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response("Not kcc account", status=status.HTTP_201_CREATED)

def getlist_Data(request):
    if request.GET.get("key_word",""):
        key_word=request.GET.get("key_word","")
        list_email=Email_email.objects.filter(Q(Subject__icontains=key_word))
    else:
        list_email=Email_email.objects.all().order_by("-id")
    if request.GET.get("status",None):
        status=request.GET.get("status",None)
        list_email=list_email.filter(Q(status=status))
    if request.GET.get("datereceive",None):
        if(request.GET.get("datereceive",None)!="Datetoreceive"):
            print("datereceive value:"+ request.GET.get("datereceive",None)  )
            datereceive=request.GET.get("datereceive",None)
            list_email=list_email.filter(Q(created__date=datereceive))
    count=0
    allEmail=Email_email.objects.all()
    for i in range(len(allEmail)):
        if allEmail[i].date_to_close==None:
            count=count+1
    return render(request,'email_uploadapi/list_data.html',{"allEmail":allEmail,"list_email":list_email,"count":count,"datereceive":request.GET.get("datereceive",None),"status":request.GET.get("status",None),"key_word":request.GET.get("key_word","")})
def email_update(request,pk):
    email=Email_email.objects.get(pk=pk)
    if request.method == "POST":
        form =EmailFormUpdate(request.POST)
        if form.is_valid():
            email.status=form.cleaned_data['status']
            email.Subject=form.cleaned_data['Subject']
            email.note=form.cleaned_data['note']
            if email.status =='close':               
                email.date_to_close=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("close")
            else :
                email.date_to_close=None
                print(email.status)
            email.save()
    return render(request,"email_uploadapi/email_update.html",{"email":email})


def email_delete(request,pk):  
    try:   
        email_delete_object = Email_email.objects.get(pk=pk)
        email_delete_object.delete()
    except Email_email.DoesNotExist:
        email_delete_object=None
    return redirect("email_api:list_data")
def home2(request):
    return render(request,"email_uploadapi/new.html")