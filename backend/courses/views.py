from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import (
    Stream, Subject, Course, Module, Lesson,
    Enrollment, LessonProgress
)
from .serializers import (
    StreamSerializer, SubjectSerializer, CourseSerializer,
    CourseDetailSerializer, ModuleSerializer, LessonSerializer,
    EnrollmentSerializer, LessonProgressSerializer
)

class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    
    @action(detail=True, methods=['get'])
    def subjects(self, request, slug=None):
        stream = self.get_object()
        subjects = stream.subjects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['stream']
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        return Subject.objects.select_related('stream')


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['subject', 'teacher', 'level', 'is_published']
    search_fields = ['title', 'description', 'teacher__first_name', 'teacher__last_name']
    ordering_fields = ['created_at', 'enrollment_count', 'price']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Course.objects.filter(is_published=True).select_related('subject', 'teacher')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        """S'inscrire à un cours"""
        course = self.get_object()
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={'is_active': True}
        )
        if created:
            return Response(
                {'message': 'Inscription réussie au cours'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'Vous êtes déjà inscrit à ce cours'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def my_progress(self, request, pk=None):
        """Récupère la progression de l'étudiant"""
        course = self.get_object()
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=course)
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data)
        except Enrollment.DoesNotExist:
            return Response(
                {'error': 'Vous n\'êtes pas inscrit à ce cours'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_courses(self, request):
        """Récupère les cours de l'utilisateur (inscriptions)"""
        enrollments = Enrollment.objects.filter(
            student=request.user,
            is_active=True
        ).select_related('course')
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)


class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course']
    
    def get_queryset(self):
        return Module.objects.filter(course__is_published=True)


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['module', 'content_type']
    
    def get_queryset(self):
        return Lesson.objects.filter(module__course__is_published=True)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_complete(self, request, pk=None):
        """Marquer une leçon comme complétée"""
        lesson = self.get_object()
        progress, created = LessonProgress.objects.update_or_create(
            student=request.user,
            lesson=lesson,
            defaults={'is_completed': True}
        )
        serializer = LessonProgressSerializer(progress)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'course', 'is_active']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Enrollment.objects.all()
        elif user.role == 'teacher':
            return Enrollment.objects.filter(course__teacher=user)
        else:
            return Enrollment.objects.filter(student=user)
