from .views import UserProgressListView, UserProgressUpdateSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'userProgress', UserProgressUpdateSet)

urlpatterns = [
    path('userProgress/', UserProgressListView.as_view(), name='userProgress-list'),
    path('', include(router.urls)),
]
