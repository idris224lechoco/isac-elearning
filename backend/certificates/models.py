from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Certificate(models.Model):
    """Certificat d'accomplissement"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='certificates')
    certificate_number = models.CharField(max_length=100, unique=True)
    pdf_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    is_verified = models.BooleanField(default=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'certificates'
        unique_together = ['student', 'course']
        indexes = [
            models.Index(fields=['certificate_number']),
            models.Index(fields=['student']),
        ]
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.title}"
