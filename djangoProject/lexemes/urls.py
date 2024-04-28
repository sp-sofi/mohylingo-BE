from django.urls import path
from .views import LexemesListView

urlpatterns = [
    path('lexemes/', LexemesListView.as_view(), name='lexemes-list'),
]
