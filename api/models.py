from django.db import models
# Create your models here.

class APIEntry(models.Model):
    endpoint = models.CharField(max_length=200)
    primary_keys = models.TextField()
    secondary_keys = models.TextField()
    category = models.CharField(max_length=200)
    file = models.FileField(upload_to='')
    