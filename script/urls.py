from django.contrib import admin
from django.urls import path, include
from script import views

urlpatterns = [

    path('', views.index, name='index'),
    path('php/', views.php, name='php'),

]