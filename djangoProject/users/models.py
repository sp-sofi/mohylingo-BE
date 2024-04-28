from django.contrib.auth.models import AbstractUser
from django.db import models
from levels.models import Level


class CustomUser(AbstractUser):
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
