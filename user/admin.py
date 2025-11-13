from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailVerificationToken, PasswordResetOTP

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_verified', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_verified', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'phone', 'address', 'zip_code')}),
        ('Permissions', {'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_verified', 'is_staff', 'is_active')}
        ),
    )
    
    readonly_fields = ['date_joined', 'last_login']



@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'created_at', 'expires_at', 'is_used', 'is_valid']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__email', 'otp_code']
    readonly_fields = ['otp_code', 'created_at', 'expires_at']
    ordering = ['-created_at']
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Valid'

@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'created_at', 'expires_at', 'is_used', 'is_valid']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__email', 'otp_code']
    readonly_fields = ['otp_code', 'created_at', 'expires_at']
    ordering = ['-created_at']
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Valid'

admin.site.register(CustomUser, CustomUserAdmin)

