from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations Supplémentaires', {'fields': ('role', 'phone', 'avatar', 'bio', 'date_of_birth', 'address', 'city', 'country', 'is_verified')}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website', 'created_at')
    search_fields = ('user__email', 'user__first_name')
