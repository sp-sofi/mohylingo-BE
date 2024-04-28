from rest_framework import serializers

from lexemes.serializers import LexemeSerializer
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    options = LexemeSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'options', 'answer', 'topic', 'level']
