from django.forms import Select, TextInput
from django_filters import FilterSet, CharFilter, BooleanFilter, DateFromToRangeFilter

from board_control.models import BoardModel, CardModel
from common.choices import YesNoChoices
from common.custom_widgets import CustomDateRangeFilterWidget


class BoardModelFilter(FilterSet):
    project = CharFilter(
        field_name="project__uuid", label="Project Id",
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
        model = BoardModel
        fields = [
            'project__uuid',
            'is_active',
            'is_deleted',
            'created_at',
        ]


class CardModelFilter(FilterSet):
    board = CharFilter(
        field_name="board", label="Board Id",
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
        model = CardModel
        fields = [
            'board',
            'is_active',
            'is_deleted',
            'created_at',
        ]
