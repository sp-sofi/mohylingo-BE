from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Question
from .serializers import QuestionSerializer


class QuestionsListView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(QuestionsListView, self).get_permissions()

    def get_queryset(self):

        queryset = Question.objects.all()
        level_id = self.request.query_params.get('level_id')
        if level_id is not None:
            queryset = queryset.filter(level_id=level_id)

        topic_id = self.request.query_params.get('topic_id')
        if topic_id is not None:
            queryset = queryset.filter(topic_id=topic_id)
        return queryset
