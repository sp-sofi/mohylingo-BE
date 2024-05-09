from django.urls import path
from .views import MessageListView, SendMessageView, ChatHistoryView

urlpatterns = [
    path('messages/', MessageListView.as_view(), name='messages-list'),
    path('send_message/', SendMessageView.as_view(), name='send_message'),
    path('chat/history/', ChatHistoryView.as_view(), name='chat_history'),
]