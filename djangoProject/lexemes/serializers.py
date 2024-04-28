from rest_framework import serializers
from .models import Lexeme


class LexemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lexeme
        fields = ['id', 'text', 'translation', 'level']
