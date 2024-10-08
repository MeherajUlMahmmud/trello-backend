from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from board_control.custom_filters import CardModelFilter
from board_control.models import CardModel
from board_control.serializers.card import CardModelSerializer
from common.custom_view import (
    CustomCreateAPIView, CustomUpdateAPIView, CustomRetrieveAPIView, CustomListAPIView,
)


class GetCardListAPIView(CustomListAPIView):
    queryset = CardModel.objects.filter(is_active=True, is_deleted=False).order_by('serial')
    serializer_class = CardModelSerializer.List
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = CardModelFilter
    search_fields = ['title', 'description', ]


class GetCardDetailsAPIView(CustomRetrieveAPIView):
    queryset = CardModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CardModelSerializer.List

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user

        if not request.user.check_object_permissions(request, instance):
            return Response({
                'detail': 'You do not have permission to perform this action'
            }, status=HTTP_403_FORBIDDEN)

        serializer = CardModelSerializer.List(instance)
        return Response({
            'data': serializer.data,
        }, status=HTTP_200_OK)


class CreateCardAPIView(CustomCreateAPIView):
    queryset = CardModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CardModelSerializer.Write

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        card = CardModel.objects.create(
            created_by=request.user,
            **validated_data
        )
        card.save()

        return Response({
            'message': 'Card created successfully.',
        }, status=HTTP_201_CREATED)


class UpdateCardDetailsAPIView(CustomUpdateAPIView):
    queryset = CardModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CardModelSerializer.Write

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user
        if not requested_user.check_object_permissions(request, instance):
            return Response({
                'message': 'You don\'t have permission to perform this action.'
            }, status=HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(
            instance, data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            updated_by=request.user,
        )
        return Response(serializer.data, status=HTTP_200_OK)
