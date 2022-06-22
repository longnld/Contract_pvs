from django.urls import re_path as url
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from .views import LoginViewMix, admin_board, settings_customer
from django.urls import path as url

app_name = "user"

password_urls = [

]

urlpatterns = [
    url(r'^$',
        RedirectView.as_view(
            pattern_name='user:login',
            permanent=False)),
    url(r'^login/$',
        LoginViewMix.as_view(
            template_name='user/login.html'),
        name='login'),
    url(r'^logout/$',
        auth_views.LogoutView.as_view(),
        name='logout'),
    url(r'admin-board$',admin_board,name="admin_board"),
    url(r'settings-customer$',settings_customer,name="settings_customer"),
    
] + password_urls