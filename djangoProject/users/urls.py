from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomAuthToken, StartNewCourseView


router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('start_new_course/', StartNewCourseView.as_view(), name='start-new-course'),
]
