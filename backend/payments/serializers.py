from rest_framework import serializers
from .models import Payment, PaymentLog

class PaymentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLog
        fields = ['id', 'status_before', 'status_after', 'message', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    logs = PaymentLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'student', 'student_name', 'course', 'course_title',
            'amount', 'currency', 'payment_method', 'phone_number',
            'status', 'transaction_id', 'operator_reference',
            'created_at', 'completed_at', 'logs'
        ]
        read_only_fields = ['id', 'created_at', 'completed_at']
