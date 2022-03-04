from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [

    path('request/', views.request, name='request'),
    path('request/confirm/', views.confirm, name='confirm'),
    path('onboard/<uidb64>/<token>/', views.onboard, name='onboard'),
    path('access/', views.access, name='access'),
    path('update/', views.update, name='update'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('exit/',views.exit , name='exit'),
    path('', views.index, name='index'),
    path('script/', views.script, name='script'),

]