from rest_framework.serializers import ModelSerializer, CharField

from workspace_control.models import WorkspaceModel


class WorkspaceModelSerializerMeta(ModelSerializer):
    class Meta:
        model = WorkspaceModel
        ref_name = 'WorkspaceModelSerializer'
        fields = [
            'title',
            'description',
        ]


class WorkspaceModelSerializer:
    class List(WorkspaceModelSerializerMeta):
        class Meta(WorkspaceModelSerializerMeta.Meta):
            fields = WorkspaceModelSerializerMeta.Meta.fields + [
                'uuid',
                'id',
            ]

    class Lite(WorkspaceModelSerializerMeta):
        class Meta(WorkspaceModelSerializerMeta.Meta):
            fields = WorkspaceModelSerializerMeta.Meta.fields + [
                'id',
                'title',
            ]

    class Write(WorkspaceModelSerializerMeta):
        title = CharField(write_only=True, required=True)
        description = CharField(write_only=True, required=False)

        class Meta(WorkspaceModelSerializerMeta.Meta):
            fields = WorkspaceModelSerializerMeta.Meta.fields + [
                'id',
            ]
