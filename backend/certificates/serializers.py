from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_stream = serializers.CharField(source='course.subject.stream.name', read_only=True)
    course_subject = serializers.CharField(source='course.subject.name', read_only=True)
    pdf_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Certificate
        fields = [
            'id', 'student', 'student_name', 'course', 'course_title',
            'course_stream', 'course_subject', 'certificate_number',
            'issued_at', 'is_verified', 'pdf_url'
        ]
        read_only_fields = [
            'id', 'certificate_number', 'issued_at', 'is_verified'
        ]
    
    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file and request:
            return request.build_absolute_uri(obj.pdf_file.url)
        return None
