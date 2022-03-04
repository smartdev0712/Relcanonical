from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from .manager import UserAccountManager
# Create your models here.

class AccountPlans(models.TextChoices):
    UNLIMITED = "UNLIMITED"
    PLATFORM = "PLATFORM"
    BUSINESS = "BUSINESS"
    ENTERPRISE = "ENTERPRISE"
    UNDEFINED = "UNDEFINED"

# # created a custom user model and set the email field as the major field
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified=models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserAccountManager()

    # unique field used to identify a user
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

class Request(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    is_email_verified=models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

class UserAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_plan = models.CharField(max_length=20 , choices=AccountPlans.choices , default=AccountPlans.choices[-1])
    date_updated = models.DateTimeField(auto_now_add=True)