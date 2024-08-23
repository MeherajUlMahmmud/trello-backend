from rest_framework.serializers import ModelSerializer, CharField

from board_control.models import BoardModel
from workspace_control.serializers.project import ProjectModelSerializer


class BoardModelSerializerMeta(ModelSerializer):
    class Meta:
        model = BoardModel
        ref_name = 'BoardModelSerializer'
        fields = [
            'project',
            'title',
        ]


class BoardModelSerializer:
    class List(BoardModelSerializerMeta):
        project = ProjectModelSerializer.List(read_only=True)

        class Meta(BoardModelSerializerMeta.Meta):
            fields = BoardModelSerializerMeta.Meta.fields + [
                'id',
                'description',
                'serial',
            ]

    class Write(BoardModelSerializerMeta):
        title = CharField(write_only=True, required=True)

        class Meta(BoardModelSerializerMeta.Meta):
            fields = BoardModelSerializerMeta.Meta.fields + [
                'id',
            ]
