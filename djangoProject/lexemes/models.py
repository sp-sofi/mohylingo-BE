from django.db import models
from levels.models import Level


class Lexeme(models.Model):
    text = models.CharField()
    translation = models.CharField()
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.text
