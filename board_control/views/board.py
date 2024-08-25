from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR,
)

from board_control.custom_filters import BoardModelFilter
from board_control.models import BoardModel
from board_control.serializers.board import BoardModelSerializer
from common.custom_permissions import AdminOrStaffUserPermission
from common.custom_view import (
    CustomCreateAPIView, CustomUpdateAPIView, CustomRetrieveAPIView, CustomListAPIView,
)


class GetBoardListAPIView(CustomListAPIView):
    queryset = BoardModel.objects.filter(is_active=True, is_deleted=False).order_by('serial')
    serializer_class = BoardModelSerializer.List
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = BoardModelFilter
    search_fields = ['title', 'description', 'project__title']


class GetBoardDetailsAPIView(CustomRetrieveAPIView):
    queryset = BoardModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = BoardModelSerializer.List

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user

        if not requested_user.check_object_permissions(request, instance):
            return Response({
                'detail': 'You do not have permission to perform this action'
            }, status=HTTP_403_FORBIDDEN)

        serializer = BoardModelSerializer.List(instance)
        return Response({
            'data': serializer.data,
        }, status=HTTP_200_OK)


class CreateBoardAPIView(CustomCreateAPIView):
    permission_classes = (AdminOrStaffUserPermission,)
    queryset = BoardModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = BoardModelSerializer.Write

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        board = BoardModel.objects.create(
            created_by=request.user,
            **validated_data
        )
        board.save()

        return Response({
            'message': 'Board created successfully.',
        }, status=HTTP_201_CREATED)


class UpdateBoardDetailsAPIView(CustomUpdateAPIView):
    queryset = BoardModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = BoardModelSerializer.Write

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            requested_user = request.user
            if not requested_user.check_object_permissions(instance):
                return Response({
                    'message': 'You don\'t have permission to perform this action.'
                }, status=HTTP_403_FORBIDDEN)

            serializer = self.serializer_class(
                instance,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save(
                    updated_by=request.user,
                    **serializer.validated_data,
                )
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                print(serializer.errors)
                return Response({
                    'details': serializer.errors,
                }, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
