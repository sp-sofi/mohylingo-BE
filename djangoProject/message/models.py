from django.db import models
from user_progress.models import UserProgress
from users.models import CustomUser


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(UserProgress, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField()

    def __str__(self):
        return self.text
