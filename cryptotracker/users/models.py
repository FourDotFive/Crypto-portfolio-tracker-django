from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=10, default='USD')
