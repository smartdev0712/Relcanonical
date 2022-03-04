from django.contrib import admin
from django.urls import path, include
from query import views

urlpatterns = [

    path('', views.complete, name='index'),
    
]
