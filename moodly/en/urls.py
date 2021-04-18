#urls.py
from django.contrib import admin  
from en import views  
from django.conf.urls import url
from django.urls import path, include
 

app_name = "main"

urlpatterns = [
    path('', views.contact, name="home"),
]