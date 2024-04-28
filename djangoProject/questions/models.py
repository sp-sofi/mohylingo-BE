from django.db import models
from levels.models import Level
from lexemes.models import Lexeme
from topics.models import Topic


class Question(models.Model):
    text = models.CharField()
    options = models.ManyToManyField(Lexeme, related_name='questions')
    answer = models.ForeignKey(Lexeme, on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.text
