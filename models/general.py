from django.db import models
from django.utils import timezone 

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)

class Industry(models.Model): 
    name = models.CharField(max_length=255)
