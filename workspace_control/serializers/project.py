from rest_framework.serializers import Serializer, ModelSerializer, CharField, ListField, IntegerField, ValidationError

from board_control.models import BoardModel
from workspace_control.models import ProjectModel
from workspace_control.serializers.workspace import WorkspaceModelSerializer


class ProjectModelSerializerMeta(ModelSerializer):
    class Meta:
        model = ProjectModel
        ref_name = 'ProjectModelSerializer'
        fields = [
            'workspace',
            'title',
            'description',
        ]


class ProjectModelSerializer:
    class List(ProjectModelSerializerMeta):
        workspace = WorkspaceModelSerializer.List(read_only=True)

        class Meta(ProjectModelSerializerMeta.Meta):
            fields = ProjectModelSerializerMeta.Meta.fields + [
                'uuid',
                'id',
                'description',
            ]

    class Write(ProjectModelSerializerMeta):
        title = CharField(write_only=True, required=True)

        class Meta(ProjectModelSerializerMeta.Meta):
            fields = ProjectModelSerializerMeta.Meta.fields + [
                'workspace',
            ]


class BoardOrderSerializer(Serializer):
    board_order = ListField(
        child=IntegerField(),
        write_only=True
    )

    def validate_board_order(self, value):
        project_uuid = self.context['project_uuid']
        board_ids = set(BoardModel.objects.filter(
            project__uuid=project_uuid,
        ).values_list('id', flat=True))

        if set(value) != board_ids:
            raise ValidationError("Invalid board IDs in the order.")
        return value

    def update(self, instance, validated_data):
        board_order = validated_data['board_order']
        BoardModel.objects.bulk_update([
            BoardModel(id=pk, serial=index)
            for index, pk in enumerate(board_order)
        ], ['serial'])
        return instance
