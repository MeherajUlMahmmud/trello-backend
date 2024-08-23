from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from common.models import BaseModel, ContactUsModel, RequestLog


class CommonAdminMixin:

    # def save_model(self, request, obj, form, change):
    #     if change:  # Only set updated_by if this is an update, not a creation
    #         obj.updated_by = request.user
    #     else:
    #         obj.created_by = request.user
    #     obj.save()

    @staticmethod
    def get_status_fields():
        return 'is_active', 'is_deleted'

    @staticmethod
    def get_history_fields():
        return 'created_at', 'updated_at', 'created_by', 'updated_by'

    def get_common_fieldsets(self):
        return (
            ('Status', {'fields': self.get_status_fields()}),
            ('History', {'fields': self.get_history_fields()}),
        )


class RawIdFieldsAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super(RawIdFieldsAdmin, self).__init__(*args, **kwargs)
        # make all ForeignKey fields use raw_id_fields
        # self.raw_id_fields = [
        #     field.name for field in self.model._meta.get_fields() if field.is_relation and field.many_to_one
        # ]

        if issubclass(self.model, BaseModel):
            primary_key = self.model._meta.pk.name
            CREATED_AT = ['created_at']
            UPDATED_AT = ['updated_at']
            IS_ACTIVE = ['is_active']
            IS_DELETED = ['is_deleted']
            timestamp_fields = CREATED_AT + UPDATED_AT
            status_fields = IS_ACTIVE + IS_DELETED
            self.list_display = [primary_key] + list(self.list_display) + CREATED_AT + IS_ACTIVE
            self.readonly_fields = list(
                self.readonly_fields) + timestamp_fields
            self.list_filter = list(self.list_filter) + CREATED_AT + status_fields
            self.list_per_page = 100


@admin.register(ContactUsModel)
class ContactUsModelAdmin(CommonAdminMixin, ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = (
        'name', 'email', 'message', 'is_checked',
    )
    search_fields = (
        'name', 'email',
    )
    list_filter = (
        'is_checked',
    )
    fieldsets = (
        (None, {'fields': (
            'name', 'email', 'message', 'is_checked',
        )}),
    )

    fieldsets += CommonAdminMixin().get_common_fieldsets()

    @staticmethod
    def message(obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message


@admin.register(RequestLog)
class RequestLogModelAdmin(CommonAdminMixin, ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = (
        'user', 'ip_address', 'endpoint', 'status_code',
    )
    search_fields = (
        'user', 'ip_address', 'endpoint', 'status_code',
    )
    list_filter = (
        'user', 'ip_address', 'endpoint', 'status_code',
    )
    fieldsets = (
        (None, {'fields': (
            'user', 'ip_address', 'endpoint', 'status_code',
        )}),
    )

    fieldsets += CommonAdminMixin().get_common_fieldsets()
