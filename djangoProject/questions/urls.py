from django.urls import path
from .views import QuestionsListView, NonLearnedQuestionsListView

urlpatterns = [
    path('questions/', QuestionsListView.as_view(), name='questions-list'),
    path('questions/nonLearned/', NonLearnedQuestionsListView.as_view(), name='nonLearnedQuestions'),
]
