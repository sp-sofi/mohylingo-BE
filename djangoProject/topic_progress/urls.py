from .views import TopicProgressView, TopicProgressUpdateSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r'topicProgress', TopicProgressUpdateSet)

urlpatterns = [
    path('', include(router.urls)),
    path('topicProgress/', TopicProgressView.as_view(), name='topicProgress-list'),
]
