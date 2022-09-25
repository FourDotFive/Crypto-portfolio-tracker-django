from django.db import models
from datetime import datetime


class User(models.Model):
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=64)


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    use_allocated_funds = models.BooleanField(default=True)
    allocated_funds = models.FloatField(null=True)


class Purchase(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    crypto = models.CharField(max_length=20)
    date = models.DateField(default=datetime.now())
    price = models.FloatField()
    amount = models.FloatField()
