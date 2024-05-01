from .models import UserProgress
from .serializer import UserProgressSerializer
from users.utils import get_user_from_auth_request, check_user_finished_course
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from questions.models import Question
from lexemes.models import Lexeme


class UserProgressView(generics.RetrieveAPIView):
    serializer_class = UserProgressSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(UserProgressView, self).get_permissions()

    def get_object(self):
        user = get_user_from_auth_request(self.request)
        if user is None:
            return Response({'error': 'Auth is required'}, status=status.HTTP_400_BAD_REQUEST)
        level_id = user.level_id
        user_progress = get_object_or_404(UserProgress, user_id=user.id, level_id=level_id)
        return user_progress


class UserProgressUpdateSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(UserProgressUpdateSet, self).get_permissions()

    @action(detail=True, methods=['put'], url_path='learnWord')
    def add_word(self, request, pk=None):
        """Adds a word to the words_learned set of a UserProgress."""
        user = get_user_from_auth_request(self.request)
        if user is None:
            return Response({'error': 'Auth is required'}, status=status.HTTP_400_BAD_REQUEST)
        level_id = user.level_id
        user_progress = get_object_or_404(UserProgress, user_id=user.id, level_id=level_id)
        word_id = request.data.get('word_id')

        if not word_id:
            return Response({'error': 'Word ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the question object based on the provided ID
        word = get_object_or_404(Lexeme, pk=word_id)

        # Add the question to the questions_learned set
        user_progress.words_learned.add(word)

        check_user_finished_course(user)

        # Return the updated topic progress
        return Response({'status': 'word added'}, status=status.HTTP_200_OK)


class CourseProgressView(generics.GenericAPIView):
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(CourseProgressView, self).get_permissions()

    def get(self, request, *args, **kwargs):
        user = request.user
        level_id = user.level_id

        total_questions = Question.objects.filter(level_id=level_id).count()
        total_lexemes = Lexeme.objects.filter(level_id=level_id).count()
        user_progress = UserProgress.objects.filter(user_id=user.id, level_id=level_id).first()

        learned_questions = user_progress.topic_progresses.filter(questions_learned__isnull=False).count()
        learned_lexemes = user_progress.words_learned.count() if user_progress else 0

        course_progress_percent =  (learned_questions + learned_lexemes) / (total_questions + total_lexemes) * 100

        return Response({
            'total_questions': total_questions,
            'learned_questions': learned_questions,
            'total_lexemes': total_lexemes,
            'learned_lexemes': learned_lexemes,
            'course_progress_percent': course_progress_percent,
        })
