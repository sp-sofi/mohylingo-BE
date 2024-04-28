from levels.models import Level
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    level_id = serializers.PrimaryKeyRelatedField(
        queryset=Level.objects.all(),
        source='level',
        write_only=True,
    )
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'level_id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.password = make_password(validated_data['password'])
        user.level = validated_data.get('level', None)
        user.save()
        return user
