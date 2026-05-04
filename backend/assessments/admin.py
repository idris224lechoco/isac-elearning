from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, Answer, Grade

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'passing_percentage', 'is_published')
    list_filter = ('is_published', 'course')
    search_fields = ('title', 'description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'question_type', 'points', 'order')
    list_filter = ('question_type', 'quiz')
    search_fields = ('question_text',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'is_correct', 'order')
    list_filter = ('is_correct',)
    search_fields = ('choice_text',)

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'attempt_number', 'score', 'is_passed', 'submitted_at')
    list_filter = ('is_passed', 'submitted_at')
    search_fields = ('student__email', 'quiz__title')
    readonly_fields = ('started_at',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'is_correct', 'points_earned')
    list_filter = ('is_correct',)
    search_fields = ('attempt__student__email', 'question__question_text')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'total_score', 'grade_letter', 'created_at')
    list_filter = ('grade_letter', 'course')
    search_fields = ('student__email', 'course__title')
