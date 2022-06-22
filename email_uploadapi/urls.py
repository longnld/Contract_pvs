from django.urls import path,include
from . import views
app_name='email_api'
urlpatterns = [
    path('infoemail', views.create_data),
    path('list_data', views.getlist_Data,name="list_data"),
    path('update_email/<int:pk>',views.email_update,name="email_update"),
    path('email_delete/<int:pk>',views.email_delete,name="email_delete"),
    path("new",views.home2)
]