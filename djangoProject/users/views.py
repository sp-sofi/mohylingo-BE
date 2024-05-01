from topic_progress.models import TopicProgress
from .models import CustomUser
from rest_framework import viewsets, status, generics, mixins
from users.utils import check_user_finished_course
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from user_progress.models import UserProgress
from topics.models import Topic


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(UserViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Password is hashed in the serializer
        token = Token.objects.create(user=user)
        data = serializer.data
        data['token'] = token.key  # Include the token in the response
        topics = Topic.objects.filter(level=user.level)
        topic_progresses = []
        for topic in topics:
            topic_progress = TopicProgress.objects.create(topic=topic)
            topic_progresses.append(topic_progress)

        user_progress = UserProgress.objects.create(user=user, level=user.level)
        user_progress.topic_progresses.set(topic_progresses)

        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

class StartNewCourseView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(StartNewCourseView, self).get_permissions()

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        is_course_finished = check_user_finished_course(user)
        if not is_course_finished:
            return Response({'error': 'The course is not finished yet'}, status=status.HTTP_400_BAD_REQUEST)
        user.level_id += 1
        user.save()
        topics = Topic.objects.filter(level=user.level)
        topic_progresses = []
        for topic in topics:
            topic_progress = TopicProgress.objects.create(topic=topic)
            topic_progresses.append(topic_progress)

        user_progress = UserProgress.objects.create(user=user, level=user.level)
        user_progress.topic_progresses.set(topic_progresses)

        return Response(self.get_serializer(user).data)
