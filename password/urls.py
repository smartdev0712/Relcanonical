from django.contrib import admin
from django.urls import path, include
from password import views

urlpatterns = [

    path('', views.index, name='index'),
    path('request/', views.request, name='request'),
    path('request/confirm/', views.confirm, name='confirm'),
    path('change/<uidb64>/<token>', views.change, name='change'),

]