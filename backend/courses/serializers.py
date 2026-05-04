from rest_framework import serializers
from .models import Stream, Subject, Course, Module, Lesson, Enrollment, LessonProgress

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color', 'created_at']


class SubjectSerializer(serializers.ModelSerializer):
    stream_name = serializers.CharField(source='stream.name', read_only=True)
    
    class Meta:
        model = Subject
        fields = ['id', 'stream', 'stream_name', 'name', 'slug', 'description', 'thumbnail', 'created_at']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'module', 'title', 'description', 'content_type',
            'content_text', 'video_url', 'video_file', 'document_file',
            'duration_minutes', 'order', 'is_free', 'created_at'
        ]


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Module
        fields = ['id', 'course', 'title', 'description', 'order', 'lessons', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    enrollment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'subject', 'subject_name', 'teacher', 'teacher_name',
            'title', 'slug', 'description', 'thumbnail', 'price',
            'duration_hours', 'level', 'is_published', 'enrollment_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_enrollment_count(self, obj):
        return obj.enrollment_count


class CourseDetailSerializer(CourseSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['modules']


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name', 'course', 'course_title',
            'progress', 'is_active', 'completed_at', 'enrolled_at'
        ]
        read_only_fields = ['id', 'enrolled_at']


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    
    class Meta:
        model = LessonProgress
        fields = [
            'id', 'student', 'lesson', 'lesson_title',
            'is_completed', 'watched_duration_seconds', 'completed_at'
        ]
