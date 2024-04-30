from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.utils import get_user_from_auth_request
from rest_framework.response import Response
from user_progress.models import UserProgress
from topic_progress.models import TopicProgress
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


class NonLearnedQuestionsListView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(NonLearnedQuestionsListView, self).get_permissions()

    def get_queryset(self):
        user = get_user_from_auth_request(self.request)
        if user is None:
            return Response({'error': 'Auth is required'}, status=status.HTTP_400_BAD_REQUEST)
        level_id = user.level_id  # assuming the user model has a level_id field
        topic_id = self.request.query_params.get('topic_id')

        user_progress = UserProgress.objects.filter(user_id=user.id, level_id=level_id).first()
        if user_progress is None:
            return Question.objects.none()

        topic_progress = user_progress.topic_progresses.filter(topic_id=topic_id).first()
        # topic_progress = TopicProgress.objects.filter(user_progress=user_progress, topic_id=topic_id).first()
        if topic_progress is None:
            return Question.objects.none()

        learned_questions = topic_progress.questions_learned.all()  # assuming the TopicProgress model has a learned_questions field

        queryset = Question.objects.filter(level_id=level_id, topic_id=topic_id).exclude(id__in=learned_questions)

        return queryset
