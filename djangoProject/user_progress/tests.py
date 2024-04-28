from django.urls import path
from .views import QuestionsListView

urlpatterns = [
    path('userProgress/', QuestionsListView.as_view(), name='userProgress-list'),
]
