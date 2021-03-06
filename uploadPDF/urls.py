"""uploadPDF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from user.views import index
urlpatterns = [
    path('admin/', admin.site.urls),    
    path(r'uploadpdf/',include('upload.urls',namespace="pdf_upload")),
    path(r'email_api/',include('email_uploadapi.urls',namespace="email_api")),
    path('',index,name="index"),
    path(r"user/",include('user.urls',namespace="user")),
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)