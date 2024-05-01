from django.db import models

from levels.models import Level
from lexemes.models import Lexeme
from topic_progress.models import TopicProgress
from users.models import CustomUser


class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    topic_progresses = models.ManyToManyField(TopicProgress, related_name='topic_progresses')
    words_learned = models.ManyToManyField(Lexeme, related_name='words_learned')
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    days_in_row = models.IntegerField(default=0)
    chat_id = models.IntegerField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.chat_id:
            UserProgress.objects.filter(id=self.id).update(chat_id=self.id)
