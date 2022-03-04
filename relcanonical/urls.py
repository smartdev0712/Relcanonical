from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [

    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('query/', include('query.urls')),
    path('password/', include('password.urls')),
    path('error/', include('error.urls')),
    path('', include('app.urls')),
    path('api/', include('api.urls')),
    path('script/', include('script.urls')),

]