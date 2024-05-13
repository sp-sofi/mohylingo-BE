from rest_framework import generics, status
from vertexai.language_models import TextGenerationModel
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user_progress.models import UserProgress
from .models import Message
from .serializers import MessageSerializer

ai_model = TextGenerationModel.from_pretrained('text-bison@001')

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
        user_progress = UserProgress.objects.get(user=self.request.user, level_id=self.request.user.level_id)
        Message.objects.create(sender=request.user, text=message, chat_id=user_progress.chat_id)
        ai_response = ai_model.predict(message).text
        Message.objects.create(sender_id=1, text=ai_response, chat_id=user_progress.chat_id)
        print(ai_response)
        return Response({'message': ai_response}, status=status.HTTP_200_OK)


class ChatHistoryView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(ChatHistoryView, self).get_permissions()

    def get_queryset(self):
        user_progress = UserProgress.objects.get(user=self.request.user, level_id=self.request.user.level_id)
        return Message.objects.filter(chat_id=user_progress.chat_id).order_by('created_at')
