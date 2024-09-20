from rest_framework.serializers import Serializer, ModelSerializer, CharField, ListField, IntegerField, ValidationError

from board_control.models import BoardModel, CardModel
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
                'uuid',
                'id',
                'description',
                'serial',
            ]

    class Write(BoardModelSerializerMeta):
        title = CharField(write_only=True, required=True)

        class Meta(BoardModelSerializerMeta.Meta):
            fields = BoardModelSerializerMeta.Meta.fields + [
            ]


class CardOrderSerializer(Serializer):
    card_order = ListField(
        child=IntegerField(),
        write_only=True
    )

    def validate_board_order(self, value):
        board_uuid = self.context['board_uuid']
        card_ids = set(CardModel.objects.filter(
            board__uuid=board_uuid,
        ).values_list('id', flat=True))

        if set(value) != card_ids:
            raise ValidationError("Invalid card IDs in the order.")
        return value

    def update(self, instance, validated_data):
        card_order = validated_data['card_order']
        CardModel.objects.bulk_update([
            CardModel(id=pk, serial=index)
            for index, pk in enumerate(card_order)
        ], ['serial'])
        return instance
