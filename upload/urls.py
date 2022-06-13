from django.urls import path
from . import views
app_name='pdf_upload'
urlpatterns = [
    path('upload', views.home, name='home'),
    path('pdf_upload',views.model_form_upload, name='model_form_upload'),
    path('PdfReading_api',views.PDFreading_api,name='reading')
]
