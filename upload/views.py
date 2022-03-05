from django.shortcuts import render, redirect
from django.conf import settings
from upload.models import Document
from upload.forms import DocumentForm
import io
import pdfplumber
from .readpdf import read

def home(request):

    return render(request, 'upload/home.html')

def model_form_upload(request):
	if request.method=='POST':
		form=DocumentForm(request.POST,request.FILES)
		if form.is_valid():
			file=request.FILES.get('document')
			lists=read(file)
			print(type(lists))
			if type(lists)==dict:
				return render(request, 'upload/model_form_upload.html', {'lists':lists})
			else:
				return render(request, 'upload/re_Check_contract.html', {'lists':lists})
	else:
		form=DocumentForm()
	return render(request,'upload/model_form_upload.html',{'form':form})
