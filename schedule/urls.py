
from django.urls import path,include
from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('book',views.schedule,name='schedule'),
    path('slots_booked', views.slots_booked, name='slots_booked'),
    path('logout', views.logout, name='logout'),

]

