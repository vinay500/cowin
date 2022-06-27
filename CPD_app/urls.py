from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path,include
from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('otp',views.otp,name='otp'),
    path('otp_verify',views.otp_verify,name='otp_verify'),
    path('logout',views.logout,name='logout'),
]

