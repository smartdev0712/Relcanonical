from django.contrib import admin

# Register your models here.
from .models import Request , CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserAccount

class CustomUserAdmin(BaseUserAdmin):
    list_display = ["email","first_name" , "last_name", "is_accepted","is_active"]
    search_fields = ['email']
    ordering = ['email']


admin.site.register(Request)
admin.site.register(CustomUser)
admin.site.register(UserAccount)