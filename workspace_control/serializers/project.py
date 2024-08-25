from rest_framework.serializers import ModelSerializer, CharField

from workspace_control.models import ProjectModel, WorkspaceModel
from workspace_control.serializers.workspace import WorkspaceModelSerializer


class ProjectModelSerializerMeta(ModelSerializer):
    class Meta:
        model = ProjectModel
        ref_name = 'ProjectModelSerializer'
        fields = [
            'workspace',
            'title',
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
        # workspace = WorkspaceModelSerializer.

        class Meta(ProjectModelSerializerMeta.Meta):
            fields = ProjectModelSerializerMeta.Meta.fields + [
                'description',
                'workspace',
            ]

        # def validate(self, attrs):
        #     workspace = attrs['workspace']
        #     workspace = WorkspaceModel.objects.filter(id=workspace).first()
        #
        #     return
