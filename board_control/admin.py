from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from common.admin import RawIdFieldsAdmin, CommonAdminMixin
from .models import BoardModel, CardModel, CardAssignmentModel


@admin.register(BoardModel)
class BoardModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = ('title', 'project', 'serial', )
    list_filter = ('project',)
    search_fields = ('title', 'description', 'project__title')
    fieldsets = (
        (None, {'fields': (
            'project', 'title', 'description', 'serial',
        )}),
    )
    fieldsets += CommonAdminMixin().get_common_fieldsets()


@admin.register(CardModel)
class CardModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = ('title', 'board', 'serial', )
    list_filter = ('board',)
    search_fields = ('title', 'description', 'board__title')
    fieldsets = (
        (None, {'fields': (
            'board', 'title', 'description', 'serial',
        )}),
    )
    fieldsets += CommonAdminMixin().get_common_fieldsets()


@admin.register(CardAssignmentModel)
class CardAssignmentModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = ('card', 'user',)
    list_filter = ('card', 'user',)
    search_fields = ('card__title', 'user__email')
    fieldsets = (
        (None, {'fields': (
            'card', 'user',
        )}),
    )
    fieldsets += CommonAdminMixin().get_common_fieldsets()
