from django.contrib import admin
from django.urls import path, include
from api import views

urlpatterns = [

    path('', views.index, name='index'),
    path('documentation/', views.documentation, name='documentation'),
    path('generate/', views.generate, name='generate'),
    path('<slug:category>/<slug:endpoint>', (views.getAPI),name="getApi"),
    path('<slug:category>/<slug:endpoint>/<slug:param>', (views.getAPI),name="getApi"),
    # path('<slug:category>/<slug:endpoint>', (views.fileUpload),name="fileUpload"),

]
