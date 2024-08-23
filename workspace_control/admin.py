from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from common.admin import RawIdFieldsAdmin, CommonAdminMixin
from .models import WorkspaceModel, WorkspaceMemberModel, ProjectModel


@admin.register(WorkspaceModel)
class WorkspaceModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = ('uuid', 'title', 'description',)
    search_fields = ('title', 'description',)
    readonly_fields = ('uuid',)
    fieldsets = (
        (None, {'fields': (
            'uuid', 'title', 'description',
        )}),
    )
    fieldsets += CommonAdminMixin().get_common_fieldsets()


@admin.register(WorkspaceMemberModel)
class WorkspaceMemberModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = ('workspace', 'user', 'role',)
    list_filter = ('role', 'workspace',)
    search_fields = ('workspace__title', 'user__email', 'role')
    fieldsets = (
        (None, {'fields': (
            'workspace', 'user', 'role',
        )}),
    )
    fieldsets += CommonAdminMixin().get_common_fieldsets()


@admin.register(ProjectModel)
class ProjectModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = ('uuid', 'title', 'workspace',)
    list_filter = ('workspace',)
    readonly_fields = ('uuid',)
    search_fields = ('title', 'description', 'workspace__title')
    fieldsets = (
        (None, {'fields': (
            'uuid', 'workspace', 'title', 'description',
        )}),
    )
    fieldsets += CommonAdminMixin().get_common_fieldsets()
