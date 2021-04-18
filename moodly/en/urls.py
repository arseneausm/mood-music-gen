#urls.py
from django.contrib import admin  
from en import views  
from django.conf.urls import url
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
  
urlpatterns = [
    path('', views.index ),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)