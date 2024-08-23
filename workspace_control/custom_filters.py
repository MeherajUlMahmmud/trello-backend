from django.forms import Select, TextInput
from django_filters import FilterSet, CharFilter, BooleanFilter, DateFromToRangeFilter

from common.choices import YesNoChoices
from common.custom_widgets import CustomDateRangeFilterWidget
from workspace_control.models import WorkspaceModel, ProjectModel


class WorkspaceModelFilter(FilterSet):
    is_active = BooleanFilter(
        field_name="is_active", label="Is Active",
        widget=Select(
            attrs={'class': 'form-control'},
            choices=YesNoChoices,
        )
    )
    is_deleted = BooleanFilter(
        field_name="is_deleted", label="Is Deleted",
        widget=Select(
            attrs={'class': 'form-control'},
            choices=YesNoChoices,
        )
    )
    created_at = DateFromToRangeFilter(
        field_name="created_at", label="Created At",
        widget=CustomDateRangeFilterWidget(),
    )

    class Meta:
        model = WorkspaceModel
        fields = [
            'is_active',
            'is_deleted',
            'created_at',
        ]


class ProjectModelFilter(FilterSet):
    uuid = CharFilter(
        field_name="uuid", label="UUID",
        widget=TextInput(attrs={'class': 'form-control'}),
    )
    workspace = CharFilter(
        field_name="workspace", label="Workspace ID",
        widget=TextInput(attrs={'class': 'form-control'}),
    )
    is_active = BooleanFilter(
        field_name="is_active", label="Is Active",
        widget=Select(
            attrs={'class': 'form-control'},
            choices=YesNoChoices,
        )
    )
    is_deleted = BooleanFilter(
        field_name="is_deleted", label="Is Deleted",
        widget=Select(
            attrs={'class': 'form-control'},
            choices=YesNoChoices,
        )
    )
    created_at = DateFromToRangeFilter(
        field_name="created_at", label="Created At",
        widget=CustomDateRangeFilterWidget(),
    )

    class Meta:
        model = ProjectModel
        fields = [
            'uuid',
            'workspace',
            'is_active',
            'is_deleted',
            'created_at',
        ]
