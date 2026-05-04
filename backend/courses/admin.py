from django.contrib import admin
from .models import Stream, Subject, Course, Module, Lesson, Enrollment, LessonProgress

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'stream', 'created_at')
    list_filter = ('stream',)
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'subject', 'price', 'is_published', 'created_at')
    list_filter = ('is_published', 'level', 'subject', 'teacher')
    search_fields = ('title', 'description')
    readonly_fields = ('slug',)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course',)
    search_fields = ('title',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'content_type', 'duration_minutes', 'is_free')
    list_filter = ('content_type', 'is_free', 'module__course')
    search_fields = ('title',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'progress', 'is_active', 'enrolled_at')
    list_filter = ('is_active', 'enrolled_at', 'course')
    search_fields = ('student__email', 'course__title')
    readonly_fields = ('enrolled_at',)

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'completed_at')
    search_fields = ('student__email', 'lesson__title')
