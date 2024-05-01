from django.urls import path
from .views import LexemesListView, NonLearnedLexemesListView

urlpatterns = [
    path('lexemes/', LexemesListView.as_view(), name='lexemes-list'),
    path('lexemes/nonLearned/', NonLearnedLexemesListView.as_view(), name='nonLearnedLexemes'),
]
