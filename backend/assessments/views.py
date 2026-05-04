from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Quiz, Question, QuizAttempt, Answer, Grade
from .serializers import (
    QuizSerializer, QuizDetailSerializer, QuestionSerializer,
    QuizAttemptSerializer, AnswerSerializer, GradeSerializer
)
from .services import QuizEvaluationService

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['course', 'is_published']
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Quiz.objects.all()
        elif user.role == 'teacher':
            return Quiz.objects.filter(course__teacher=user)
        else:
            return Quiz.objects.filter(is_published=True)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuizDetailSerializer
        return QuizSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['quiz', 'question_type']
    
    def get_queryset(self):
        return Question.objects.filter(quiz__is_published=True)


class QuizAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['quiz', 'student', 'is_passed']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return QuizAttempt.objects.all()
        elif user.role == 'teacher':
            return QuizAttempt.objects.filter(quiz__course__teacher=user)
        else:
            return QuizAttempt.objects.filter(student=user)
    
    def create(self, request, *args, **kwargs):
        """Créer une nouvelle tentative de quiz"""
        quiz_id = request.data.get('quiz_id')
        try:
            from courses.models import Enrollment
            from django.shortcuts import get_object_or_404
            from courses.models import Course
            
            quiz = get_object_or_404(Quiz, id=quiz_id)
            course = quiz.course
            
            # Vérifier que l'utilisateur est inscrit
            enrollment = Enrollment.objects.get(student=request.user, course=course)
            
            # Vérifier le nombre de tentatives
            attempt_count = QuizAttempt.objects.filter(
                student=request.user,
                quiz=quiz
            ).count()
            
            if attempt_count >= quiz.attempts_allowed:
                return Response(
                    {'error': f'Nombre maximum de tentatives atteint ({quiz.attempts_allowed})'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            attempt = QuizAttempt.objects.create(
                quiz=quiz,
                student=request.user,
                attempt_number=attempt_count + 1
            )
            
            serializer = self.get_serializer(attempt)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Soumettre une tentative et obtenir le résultat"""
        attempt = self.get_object()
        
        result = QuizEvaluationService.evaluate_quiz_attempt(attempt)
        
        return Response({
            'message': 'Quiz soumis avec succès',
            'result': result,
            'attempt': QuizAttemptSerializer(attempt).data
        })


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['attempt', 'question', 'is_correct']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Answer.objects.all()
        else:
            return Answer.objects.filter(attempt__student=user)
    
    def create(self, request, *args, **kwargs):
        """Créer/Mettre à jour une réponse"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'course', 'grade_letter']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Grade.objects.all()
        elif user.role == 'teacher':
            return Grade.objects.filter(course__teacher=user)
        else:
            return Grade.objects.filter(student=user)
