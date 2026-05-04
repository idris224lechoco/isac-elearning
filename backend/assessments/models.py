from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Quiz(models.Model):
    """Quiz/Évaluation"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    passing_percentage = models.IntegerField(default=70)
    duration_minutes = models.IntegerField(default=60)
    attempts_allowed = models.IntegerField(default=3)
    show_correct_answers = models.BooleanField(default=True)
    shuffle_questions = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'quizzes'
        unique_together = ['course', 'title']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    """Question de quiz"""
    QUESTION_TYPES = [
        ('mcq', 'Choix Multiple'),
        ('text', 'Réponse Ouverte'),
        ('true_false', 'Vrai/Faux'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    points = models.IntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'
        ordering = ['quiz', 'order']
        unique_together = ['quiz', 'order']
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"


class Choice(models.Model):
    """Choix pour une question MCQ"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'choices'
        ordering = ['question', 'order']
        unique_together = ['question', 'order']
    
    def __str__(self):
        return f"{self.question.question_text[:50]} - {self.choice_text[:50]}"


class QuizAttempt(models.Model):
    """Tentative de quiz par un étudiant"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    attempt_number = models.PositiveIntegerField(default=1)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percentage = models.IntegerField(default=0)
    is_passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'quiz_attempts'
        unique_together = ['quiz', 'student', 'attempt_number']
        indexes = [
            models.Index(fields=['student', 'is_passed']),
        ]
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.quiz.title} (Tentative {self.attempt_number})"


class Answer(models.Model):
    """Réponse d'un étudiant à une question"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, blank=True, null=True)
    text_answer = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(default=False, null=True)
    points_earned = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'answers'
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt.student.get_full_name()} - {self.question.question_text[:50]}"


class Grade(models.Model):
    """Note finale pour un cours"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='grades')
    total_score = models.DecimalField(max_digits=5, decimal_places=2)
    grade_letter = models.CharField(max_length=2, choices=[
        ('A', 'A (90-100)'),
        ('B', 'B (80-89)'),
        ('C', 'C (70-79)'),
        ('D', 'D (60-69)'),
        ('F', 'F (0-59)'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grades'
        unique_together = ['student', 'course']
        indexes = [
            models.Index(fields=['student', 'course']),
        ]
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.title}: {self.grade_letter}"
