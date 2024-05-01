from .views import UserProgressView, UserProgressUpdateSet, CourseProgressView
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'userProgress', UserProgressUpdateSet)

urlpatterns = [
    path('userProgress/', UserProgressView.as_view(), name='userProgress'),
    path('courseProgress/', CourseProgressView.as_view(), name='course-progress'),
    path('', include(router.urls)),
]
