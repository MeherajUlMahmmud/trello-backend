from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from board_control.models import CardAssignmentModel
from board_control.serializers.card_assignment import CardAssignmentModelSerializer
from common.custom_view import (
    CustomCreateAPIView, CustomUpdateAPIView, CustomRetrieveAPIView, CustomListAPIView,
)


class GetCardAssignmentListAPIView(CustomListAPIView):
    queryset = CardAssignmentModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CardAssignmentModelSerializer.List
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['card__title', 'user__first_name', 'user__last_name']


class GetCardAssignmentDetailsAPIView(CustomRetrieveAPIView):
    queryset = CardAssignmentModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CardAssignmentModelSerializer.List

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user

        if not requested_user.check_object_permissions(instance):
            return Response({
                'detail': 'You do not have permission to perform this action'
            }, status=HTTP_403_FORBIDDEN)

        serializer = CardAssignmentModelSerializer.List(instance)
        return Response({
            'data': serializer.data,
        }, status=HTTP_200_OK)


class CreateCardAssignmentAPIView(CustomCreateAPIView):
    queryset = CardAssignmentModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CardAssignmentModelSerializer.Write

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        card_assignment = CardAssignmentModel.objects.create(
            created_by=request.user,
            **validated_data
        )
        card_assignment.save()

        return Response({
            'message': 'Card Assignment created successfully.',
        }, status=HTTP_201_CREATED)


class UpdateCardAssignmentDetailsAPIView(CustomUpdateAPIView):
    queryset = CardAssignmentModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CardAssignmentModelSerializer.Write

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user

        if not requested_user.check_object_permissions(instance):
            return Response({
                'message': 'You don\'t have permission to perform this action.'
            }, status=HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(
            instance, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            updated_by=request.user,
        )
        return Response(serializer.data, status=HTTP_200_OK)
