from rest_framework import generics
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
