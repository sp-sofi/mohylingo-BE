from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Message
from .serializers import MessageSerializer


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(MessageListView, self).get_permissions()

    def get_queryset(self):
        """
        Optionally restricts the returned lexemes to a given level,
        by filtering against a 'level_id' query parameter in the URL.
        """
        queryset = Message.objects.all()
        level_id = self.request.query_params.get('level_id')
        if level_id is not None:
            queryset = queryset.filter(level_id=level_id)
        return queryset
