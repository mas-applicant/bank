from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length = 100)
    inn = models.CharField(max_length = 12)
    money = models.FloatField()
