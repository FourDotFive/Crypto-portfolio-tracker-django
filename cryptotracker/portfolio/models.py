from django.db import models
from datetime import datetime

from django.contrib.auth import get_user_model

User = get_user_model()


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.CharField(max_length=20)
    date = models.DateField(default=datetime.now())
    price = models.FloatField()
    amount = models.FloatField()


class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.CharField(max_length=20)
    date = models.DateField(default=datetime.now())
    price = models.FloatField()
    amount = models.FloatField()
