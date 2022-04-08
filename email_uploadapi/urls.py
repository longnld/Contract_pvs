from django.urls import path
from .views import Email_email_View
urlpatterns = [
    path('infoemail', Email_email_View.as_view()),
]