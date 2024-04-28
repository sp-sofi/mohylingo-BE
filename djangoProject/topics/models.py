from django.db import models
from levels.models import Level


class Topic(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
