from rest_framework.serializers import ModelSerializer, CharField

from user_control.serializers.user import UserModelSerializer
from board_control.models import CardAssignmentModel
from board_control.serializers.card import CardModelSerializer


class CardAssignmentModelSerializerMeta(ModelSerializer):
    class Meta:
        model = CardAssignmentModel
        ref_name = 'CardAssignmentModelSerializer'
        fields = [
            'card',
            'user',
        ]


class CardAssignmentModelSerializer:
    class List(CardAssignmentModelSerializerMeta):
        card = CardModelSerializer.List(read_only=True)
        user = UserModelSerializer.Lite(read_only=True)

        class Meta(CardAssignmentModelSerializerMeta.Meta):
            fields = CardAssignmentModelSerializerMeta.Meta.fields + [
                'id',
            ]

    class Write(CardAssignmentModelSerializerMeta):
        card = CharField(write_only=True, required=True)
        user = CharField(write_only=True, required=True)

        class Meta(CardAssignmentModelSerializerMeta.Meta):
            fields = CardAssignmentModelSerializerMeta.Meta.fields + [
                'id',
            ]
