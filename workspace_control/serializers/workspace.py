from rest_framework.serializers import ModelSerializer, CharField, ImageField

from workspace_control.models import WorkspaceModel


class WorkspaceModelSerializerMeta(ModelSerializer):
    class Meta:
        model = WorkspaceModel
        ref_name = 'WorkspaceModelSerializer'
        fields = [
            'title',
            'description',
            'image',
        ]


class WorkspaceModelSerializer:
    class List(WorkspaceModelSerializerMeta):
        class Meta(WorkspaceModelSerializerMeta.Meta):
            fields = WorkspaceModelSerializerMeta.Meta.fields + [
                'uuid',
                'id',
            ]

    class Write(WorkspaceModelSerializerMeta):
        title = CharField(write_only=True, required=True)
        image = ImageField(required=False)

        class Meta(WorkspaceModelSerializerMeta.Meta):
            fields = WorkspaceModelSerializerMeta.Meta.fields + [
                'image'
            ]
