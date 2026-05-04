from django.contrib import admin
from .models import Payment, PaymentLog

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('student__email', 'course__title', 'transaction_id')
    readonly_fields = ('transaction_id', 'created_at', 'completed_at')

@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ('payment', 'status_before', 'status_after', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('payment__transaction_id', 'message')
    readonly_fields = ('created_at',)
