
from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from.models import Email_email,UploadFile
from .serializers import Email_email_Serializer
from rest_framework.decorators import api_view
import datetime
from django.db.models import Q
from.forms import EmailFormUpdate
# Create your views here.

  
@api_view(['POST'])
def create_data(request):
    Subject= request.data['Subject']
    data_email = Email_email.objects.create(Subject=Subject)
    for f in request.data.getlist('Attachments'):
        file = UploadFile.objects.create(file=f)
        data_email.Attachments.add(file)
    data_email.created=datetime.datetime.now()
    print("date email created",data_email.created)
    data_email.save()
    
    serializer = Email_email_Serializer(data_email)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)
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
    return render(request,'email_uploadapi/list_data.html',{"list_email":list_email,"count":count,"datereceive":request.GET.get("datereceive",None),"status":request.GET.get("status",None),"key_word":request.GET.get("key_word","")})
def email_update(request,pk):
    email=Email_email.objects.get(pk=pk)
    if request.method == "POST":
        form =EmailFormUpdate(request.POST)
        if form.is_valid():
            email.status=form.cleaned_data['status']
            email.Subject=form.cleaned_data['Subject']
            email.note=form.cleaned_data['note']
            if email.status =='close':               
                email.date_to_close=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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