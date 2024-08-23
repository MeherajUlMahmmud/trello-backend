from rest_framework.serializers import ModelSerializer, CharField

from board_control.models import CardModel
from board_control.serializers.board import BoardModelSerializer


class CardModelSerializerMeta(ModelSerializer):
    class Meta:
        model = CardModel
        ref_name = 'CardModelSerializer'
        fields = [
            'board',
            'title',
        ]


class CardModelSerializer:
    class List(CardModelSerializerMeta):
        board = BoardModelSerializer.List(read_only=True)

        class Meta(CardModelSerializerMeta.Meta):
            fields = CardModelSerializerMeta.Meta.fields + [
                'id',
                'description',
                'serial',
            ]

    class Write(CardModelSerializerMeta):
        title = CharField(write_only=True, required=True)
        description = CharField(write_only=True, required=False)

        class Meta(CardModelSerializerMeta.Meta):
            fields = CardModelSerializerMeta.Meta.fields + [
                'id',
            ]
