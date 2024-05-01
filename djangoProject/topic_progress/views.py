from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.utils import get_user_from_auth_request, check_user_finished_course
from .models import TopicProgress, Question
from .serializers import TopicProgressSerializer
from user_progress.models import UserProgress

class TopicProgressListView(generics.ListAPIView):
    serializer_class = TopicProgressSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(TopicProgressView, self).get_permissions()

    def get_queryset(self):
        queryset = TopicProgress.objects.all()
        return queryset


class TopicProgressUpdateSet(viewsets.ModelViewSet):
    queryset = TopicProgress.objects.all()
    serializer_class = TopicProgressSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(TopicProgressUpdateSet, self).get_permissions()

    @action(detail=True, methods=['put'], url_path='learnQuestion')
    def add_question(self, request, pk=None):
        user = get_user_from_auth_request(self.request)
        if user is None:
            return Response({'error': 'Auth is required'}, status=status.HTTP_400_BAD_REQUEST)
        """Adds a question to the questions_learned set of a TopicProgress."""
        topic_progress = get_object_or_404(TopicProgress, pk=pk)
        question_id = request.data.get('question_id')

        if not question_id:
            return Response({'error': 'Question ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the question object based on the provided ID
        question = get_object_or_404(Question, pk=question_id)

        # Add the question to the questions_learned set
        topic_progress.questions_learned.add(question)

        check_user_finished_course(user)

        # Return the updated topic progress
        return Response({'status': 'question added'}, status=status.HTTP_200_OK)


class TopicProgressView(generics.RetrieveAPIView):
    serializer_class = TopicProgressSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(TopicProgressView, self).get_permissions()

    def get_object(self):
        user = get_user_from_auth_request(self.request)
        if user is None:
            return Response({'error': 'Auth is required'}, status=status.HTTP_400_BAD_REQUEST)
        topic_progress_id = self.request.query_params.get('id')
        level_id = user.level_id
        user_progress = get_object_or_404(UserProgress, user_id=user.id, level_id=level_id)
        topic_progress = user_progress.topic_progresses.filter(id=topic_progress_id).first()
        return topic_progress
