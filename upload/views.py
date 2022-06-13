from django.shortcuts import render, redirect
from django.conf import settings
from upload.models import Document
from upload.forms import DocumentForm
import io
import pdfplumber
from .readpdf import read
from rest_framework.response import Response
from rest_framework.decorators import api_view
def home(request):

    return render(request, 'upload/home.html')

def model_form_upload(request):
	if request.method=='POST':
		form=DocumentForm(request.POST,request.FILES)
		if form.is_valid():
			file=request.FILES.get('document')
			print(file)
			lists=read(file)
			print(file)
			if type(lists)==dict:
				return render(request, 'upload/model_form_upload.html', {'lists':lists})
			else:
				return render(request, 'upload/re_Check_contract.html', {'lists':lists})
	else:
		form=DocumentForm()
	return render(request,'upload/model_form_upload.html',{'form':form})
@api_view(["GET"])
def PDFreading_api(request):
	if request.method == "GET":	
		print(request.GET.get('file'))	
		lists=read(filename=request.GET.get('file'))
		print(lists)
	return Response({"lists":lists})