from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StreamViewSet, SubjectViewSet, CourseViewSet, ModuleViewSet,
    LessonViewSet, EnrollmentViewSet
)

router = DefaultRouter()
router.register(r'streams', StreamViewSet, basename='stream')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'modules', ModuleViewSet, basename='module')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
]
