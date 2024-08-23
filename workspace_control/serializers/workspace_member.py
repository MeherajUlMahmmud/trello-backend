from rest_framework.serializers import ModelSerializer, CharField
from user_control.serializers.user import UserModelSerializer
from workspace_control.models import WorkspaceMemberModel
from workspace_control.serializers.workspace import WorkspaceModelSerializer


class WorkspaceMemberModelSerializerMeta(ModelSerializer):
    class Meta:
        model = WorkspaceMemberModel
        ref_name = 'WorkspaceMemberModelSerializer'
        fields = [
            'workspace',
            'user',
            'role',
        ]


class WorkspaceMemberModelSerializer:
    class List(WorkspaceMemberModelSerializerMeta):
        workspace = WorkspaceModelSerializer.List(read_only=True)
        user = UserModelSerializer.Lite(read_only=True)

        class Meta(WorkspaceMemberModelSerializerMeta.Meta):
            fields = WorkspaceMemberModelSerializerMeta.Meta.fields + [
                'id',
            ]

    class Write(WorkspaceMemberModelSerializerMeta):
        workspace = CharField(write_only=True, required=True)
        user = CharField(write_only=True, required=True)

        class Meta(WorkspaceMemberModelSerializerMeta.Meta):
            fields = WorkspaceMemberModelSerializerMeta.Meta.fields + [
                'id',
            ]
