from django.urls import path
from .views import Email_email_View
urlpatterns = [
    path('email_upload', Email_email_View.as_view()),
]