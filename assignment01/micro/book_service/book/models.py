from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
