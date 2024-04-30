from .views import TopicProgressListView, TopicProgressUpdateSet, TopicProgressView
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r'topicProgress', TopicProgressUpdateSet)

urlpatterns = [
    path('topicProgress/', TopicProgressView.as_view(), name='topicProgress-view'),
    path('topicProgress/list/', TopicProgressListView.as_view(), name='topicProgress-list'),
    path('', include(router.urls)),
]
