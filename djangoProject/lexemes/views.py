from rest_framework import generics
from user_progress.models import UserProgress
from rest_framework.response import Response
from users.utils import get_user_from_auth_request
from rest_framework.permissions import IsAuthenticated

from .models import Lexeme
from .serializers import LexemeSerializer


class LexemesListView(generics.ListAPIView):
    serializer_class = LexemeSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(LexemesListView, self).get_permissions()

    def get_queryset(self):
        """
        Optionally restricts the returned lexemes to a given level,
        by filtering against a 'level_id' query parameter in the URL.
        """
        queryset = Lexeme.objects.all()
        level_id = self.request.query_params.get('level_id')
        if level_id is not None:
            queryset = queryset.filter(level_id=level_id)
        return queryset


class NonLearnedLexemesListView(generics.ListAPIView):
    serializer_class = LexemeSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(NonLearnedLexemesListView, self).get_permissions()

    def get_queryset(self):
        user = get_user_from_auth_request(self.request)
        if user is None:
            return Response({'error': 'Auth is required'}, status=status.HTTP_400_BAD_REQUEST)
        level_id = user.level_id

        user_progress = UserProgress.objects.filter(user_id=user.id, level_id=level_id).first()
        if user_progress is None:
            return Lexeme.objects.none()

        words_learned = user_progress.words_learned.all()

        queryset = Lexeme.objects.filter(level_id=level_id).exclude(id__in=words_learned)

        return queryset

    def list(self, request, *args, **kwargs):
        user = self.request.user
        level_id = user.level_id  # assuming the user model has a level_id field

        total_lexemes = Lexeme.objects.filter(level_id=level_id).count()

        response = super().list(request, *args, **kwargs)

        return Response({
            'non_learned_lexemes': response.data,
            'total_lexemes': total_lexemes
         })
