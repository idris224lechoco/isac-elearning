from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizAttempt, Answer, Grade

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'choice_text', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'quiz', 'question_text', 'question_type',
            'points', 'order', 'explanation', 'choices'
        ]


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            'id', 'course', 'title', 'description', 'passing_percentage',
            'duration_minutes', 'attempts_allowed', 'is_published',
            'created_at'
        ]


class QuizDetailSerializer(QuizSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta(QuizSerializer.Meta):
        fields = QuizSerializer.Meta.fields + ['questions']


class AnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    
    class Meta:
        model = Answer
        fields = [
            'id', 'attempt', 'question', 'question_text',
            'selected_choice', 'text_answer', 'is_correct',
            'points_earned', 'created_at'
        ]


class QuizAttemptSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'quiz', 'quiz_title', 'student', 'student_name',
            'attempt_number', 'score', 'percentage', 'is_passed',
            'started_at', 'submitted_at', 'answers'
        ]
        read_only_fields = ['id', 'started_at', 'submitted_at']


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Grade
        fields = [
            'id', 'student', 'student_name', 'course', 'course_title',
            'total_score', 'grade_letter', 'created_at'
        ]
