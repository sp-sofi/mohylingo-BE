from .models import UserProgress
from .serializer import UserProgressSerializer
from users.utils import get_user_from_auth_request
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from lexemes.models import Lexeme


class UserProgressListView(generics.ListAPIView):
    serializer_class = UserProgressSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(UserProgressListView, self).get_permissions()

    def get_queryset(self):
        queryset = UserProgress.objects.all()
        user = get_user_from_auth_request(self.request)
        print('user', user)
        if user is None:
            return Response({'error': 'Auth is required'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = queryset.filter(user_id=user.id)

        level_id = self.request.query_params.get('level_id')
        if level_id is not None:
            queryset = queryset.filter(level_id=level_id)

        return queryset


class UserProgressUpdateSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer

    @action(detail=True, methods=['put'], url_path='learnWord')
    def add_word(self, request, pk=None):
        """Adds a word to the words_learned set of a UserProgress."""
        user_progress = get_object_or_404(UserProgress, pk=pk)
        word_id = request.data.get('word_id')

        if not word_id:
            return Response({'error': 'Word ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the question object based on the provided ID
        word = get_object_or_404(Lexeme, pk=word_id)

        # Add the question to the questions_learned set
        user_progress.words_learned.add(word)

        # Return the updated topic progress
        return Response({'status': 'word added'}, status=status.HTTP_200_OK)

