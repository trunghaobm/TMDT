from itertools import chain
from operator import mod, truediv
from django.db import models

# Create your models here.
class category(models.Model):
    id = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=100)
    count = models.CharField(max_length=100)
        