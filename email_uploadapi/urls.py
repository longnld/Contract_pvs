from django.urls import path,include
from . import views
app_name='email_api'
urlpatterns = [
    path('infoemail', views.create_data),
    path('list_data', views.getlist_Data,name="list_data"),
    path('search_email_in_hr',views.search_email_in_hr,name="search_email_in_hr"),
    path('update_email/<int:pk>',views.email_update,name="email_update"),
    path('email_delete/<int:pk>',views.email_delete,name="email_delete"),
]