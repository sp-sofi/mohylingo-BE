from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user_progress.models import UserProgress
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

class SendMessageView(APIView):
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(SendMessageView, self).get_permissions()

    def post(self, request, *args, **kwargs):
        message = request.data.get('message')
        if not message:
            return Response({'message': 'No message provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the user's message to the database
        user_progress = UserProgress.objects.get(user=self.request.user)
        user_message = Message.objects.create(user=request.user, message=message, chat_id=user_progress.chat_id)

        # Generate a response using the AI model
        # ai_response = generate_ai_response(message)  # replace this with your AI model

        # Save the AI's response to the database
        # ai_message = Message.objects.create(user=None, message=ai_response)

        return Response({'message': ai_response}, status=status.HTTP_200_OK)


class ChatHistoryView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(ChatHistoryView, self).get_permissions()

    def get_queryset(self):
        user_progress = UserProgress.objects.get(user=self.request.user)
        return Message.objects.filter(chat_id=user_progress.chat_id).order_by('-timestamp')
