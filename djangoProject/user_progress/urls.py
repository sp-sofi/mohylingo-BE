from .views import UserProgressView, UserProgressUpdateSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'userProgress', UserProgressUpdateSet)

urlpatterns = [
    path('userProgress/', UserProgressView.as_view(), name='userProgress'),
    path('', include(router.urls)),
]
