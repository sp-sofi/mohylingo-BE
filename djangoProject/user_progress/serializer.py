from rest_framework import serializers

from topic_progress.serializers import TopicProgressSerializer
from .models import UserProgress


class UserProgressSerializer(serializers.ModelSerializer):
    topic_progresses = TopicProgressSerializer(many=True, read_only=True)

    class Meta:
        model = UserProgress
        fields = ['id', 'user', 'topic_progresses', 'words_learned', 'level', 'days_in_row', 'chat_id']
