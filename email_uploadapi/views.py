
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
from django.utils import timezone
# Create your views here.
def index(request):
    return render(request,"index.html")
  
@api_view(['POST'])
def create_data(request):
    Subject= request.data['Subject']
    data_email = Email_email.objects.create(Subject=Subject)
    for f in request.data.getlist('Attachments'):
        file = UploadFile.objects.create(file=f)
        data_email.Attachments.add(file)
    data_email.created=datetime.datetime.now()
    print(data_email.created)
    data_email.save()
    
    serializer = Email_email_Serializer(data_email)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)
def getlist_Data(request):
    if request.GET.get("EmailId",None):
        EmailId=int(request.GET.get("EmailId"))
        list_email=Email_email.objects.filter(Q(pk=EmailId))
    else:
        list_email=Email_email.objects.all().order_by("-id")
    if request.GET.get("EmailStatus",None):
        EmailStatus=request.GET.get("EmailStatus")
        list_email=list_email.filter(Q(status=EmailStatus))
    print(request.GET.get("EmailId",None))
    print(request.GET.get("status",None))    
    
    return render(request,'email_uploadapi/list_data.html',{"list_email":list_email,"EmailId":request.GET.get("EmailId",None),"EmailStatus":request.GET.get("EmailStatus",None)})
@api_view(["GET"])
def search_email_in_hr(request):

    if request.method == "GET":
        key_word = request.GET.get("key_word")
        if key_word:
            Subjects = Email_email.objects.filter(Q(Subject__icontains=key_word))
        else:
            Subjects = Email_email.objects.all().order_by('-id')
        data_resp = ""
        
        for Subject in Subjects:
                if Subject.status=="close":
                    data_resp += f'''<tr class="table-success">
                                    <td ><a href="update_email/{Subject.pk}"> {Subject.pk}</a></td>
                                    <td > {Subject.Subject}</td>
                                    <td>

                                    '''
                elif Subject.status=="processing":
                    data_resp += f'''<tr class="table-warning">
                                    <td ><a href="update_email/{Subject.pk}"> {Subject.pk}</a></td>
                                    <td > {Subject.Subject}</td>
                                    <td>

                                    '''
                elif Subject.status=="open":
                    data_resp += f'''<tr class="table-danger">
                                    <<td ><a href="update_email/{Subject.pk}"> {Subject.pk}</a></td>
                                    <td > {Subject.Subject}</td>
                                    <td>

                                    '''
                else:
                    data_resp += f'''<tr>
                                    <td ><a href="update_email/{Subject.pk}"> {Subject.pk}</a></td>
                                    <td > {Subject.Subject}</td>
                                    <td>
                                    '''
                for attach in Subject.Attachments.all():
                    data_resp +=f'''<a href="/media/{attach}">{attach}</a><br>'''
                
                if Subject.created:
                    raw_time=str(Subject.created.date())
                    time=raw_time[8:10]+"/"+raw_time[5:7]+"/"+raw_time[0:4] #date/month/year
                    data_resp+= '''</td><td>{}</td>'''.format(time)
                    #data_resp+= '''</td><td>{}</td></tr>'''.format(datetime.datetime.strptime(str(Subject.created),"%d/%m/%Y %H %I"))
                else:
                    data_resp+='''<td></td>'''
                if Subject.date_to_close:
                    raw_time=str(Subject.date_to_close.date())
                    time=raw_time[8:10]+"/"+raw_time[5:7]+"/"+raw_time[0:4] #date/month/year

                    print(time)
                    data_resp+= '''<td>{}</td>'''.format(time)
                else:
                    data_resp+='''<td></td>'''
                data_resp+=f'''<td >{Subject.status}</td>'''
                data_resp+='''<td></td></tr>'''
        return Response({"data_resp":data_resp})
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
                print("date"+str(email.date_to_close))
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
@api_view(["GET"])
def filter_status(request):
    if request.method == "GET":
        status = request.GET.get("status")
        print(status)
        if status:
            Subjects = Email_email.objects.filter(Q(status=status))
        else:
            Subjects = Email_email.objects.all().order_by('-id')
        print(Subjects)
        data_resp = ""
        
        for Subject in Subjects:
                if Subject.status=="close":
                    data_resp += f'''<tr class="table-success">
                                    <td ><a href="update_email/{Subject.pk}"> {Subject.pk}</a></td>
                                    <td > {Subject.Subject}</td>
                                    <td>

                                    '''
                elif Subject.status=="processing":
                    data_resp += f'''<tr class="table-warning">
                                    <td ><a href="update_email/{Subject.pk}"> {Subject.pk}</a></td>
                                    <td > {Subject.Subject}</td>
                                    <td>

                                    '''
                elif Subject.status=="open":
                    data_resp += f'''<tr class="table-danger">
                                    <<td ><a href="update_email/{Subject.pk}"> {Subject.pk}</a></td>
                                    <td > {Subject.Subject}</td>
                                    <td>

                                    '''
                else:
                    data_resp += f'''<tr>
                                    <td ><a href="update_email/{Subject.pk}"> {Subject.pk}</a></td>
                                    <td > {Subject.Subject}</td>
                                    <td>
                                    '''
                for attach in Subject.Attachments.all():
                    data_resp +=f'''<a href="/media/{attach}">{attach}</a><br>'''
                
                if Subject.created:
                    raw_time=str(Subject.created.date())
                    time=raw_time[8:10]+"/"+raw_time[5:7]+"/"+raw_time[0:4] #date/month/year
                    data_resp+= '''</td><td>{}</td>'''.format(time)
                    #data_resp+= '''</td><td>{}</td></tr>'''.format(datetime.datetime.strptime(str(Subject.created),"%d/%m/%Y %H %I"))
                else:
                    data_resp+='''<td></td>'''
                if Subject.date_to_close:
                    raw_time=str(Subject.date_to_close.date())
                    time=raw_time[8:10]+"/"+raw_time[5:7]+"/"+raw_time[0:4] #date/month/year

                    print(time)
                    data_resp+= '''<td>{}</td>'''.format(time)
                else:
                    data_resp+='''<td></td>'''
                data_resp+=f'''<td >{Subject.status}</td>'''
                data_resp+='''<td></td></tr>'''
        return Response({"data_resp":data_resp})