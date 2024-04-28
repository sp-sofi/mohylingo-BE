from rest_framework import generics
from .models import Topic
from rest_framework.permissions import IsAuthenticated
from .serializers import TopicSerializer


class TopicListView(generics.ListAPIView):
    serializer_class = TopicSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(TopicListView, self).get_permissions()

    def get_queryset(self):
        """
        Optionally restricts the returned topics to a given level,
        by filtering against a 'level_id' query parameter in the URL.
        """
        queryset = Topic.objects.all()
        level_id = self.request.query_params.get('level_id')
        if level_id is not None:
            queryset = queryset.filter(level_id=level_id)
        return queryset
