from rest_framework import serializers
from .models import TopicProgress
from topics.serializers import TopicSerializer


class TopicProgressSerializer(serializers.ModelSerializer):
    questions_total = serializers.ReadOnlyField()
    topic = TopicSerializer(read_only=True)
    class Meta:
        model = TopicProgress
        fields = ['id', 'topic', 'questions_learned', 'questions_total']
