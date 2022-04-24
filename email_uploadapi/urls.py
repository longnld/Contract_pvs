from django.urls import path
from . import views
urlpatterns = [
    path('infoemail', views.create_data),
    path('list_data', views.getlist_Data),
]