from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


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
