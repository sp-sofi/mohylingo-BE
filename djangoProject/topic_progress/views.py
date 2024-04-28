from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import TopicProgress, Question
from .serializers import TopicProgressSerializer

class TopicProgressView(generics.ListAPIView):
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

    @action(detail=True, methods=['put'], url_path='learnQuestion')
    def add_question(self, request, pk=None):
        """Adds a question to the questions_learned set of a TopicProgress."""
        topic_progress = get_object_or_404(TopicProgress, pk=pk)
        question_id = request.data.get('question_id')

        if not question_id:
            return Response({'error': 'Question ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the question object based on the provided ID
        question = get_object_or_404(Question, pk=question_id)

        # Add the question to the questions_learned set
        topic_progress.questions_learned.add(question)

        # Return the updated topic progress
        return Response({'status': 'question added'}, status=status.HTTP_200_OK)