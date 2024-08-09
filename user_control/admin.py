from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from common.admin import RawIdFieldsAdmin, CommonAdminMixin
from .models import UserModel


@admin.register(UserModel)
class UserModelAdmin(CommonAdminMixin, ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'is_superuser',
    )
    list_filter = (
        'is_verified',  'is_staff', 'is_admin', 'is_superuser',
    )
    search_fields = (
        'email',
    )
    readonly_fields = (
        'password',
        'reset_password_token',
        'reset_password_token_expiry',
    )
    fieldsets = (
        (None, {'fields': (
            'email', 'first_name', 'last_name',
            'profile_picture', 'otp', 'otp_expiry',
            'groups', 'user_permissions',
        )}),
        ('Secret', {'fields': (
            'password', 'reset_password_token', 'reset_password_token_expiry',
        )}),
        ('Permissions', {'fields': (
            'is_verified', 'is_staff', 'is_admin', 'is_superuser',
        )}),
    )
    fieldsets += CommonAdminMixin().get_common_fieldsets()

    actions = ['reset_password']

    def reset_password(self, request, queryset):
        for user in queryset:
            user.reset_password()
        self.message_user(request, 'Password reset successfully')

    reset_password.short_description = 'Reset Password'
