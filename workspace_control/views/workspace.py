from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from common.custom_view import (
    CustomCreateAPIView, CustomUpdateAPIView, CustomRetrieveAPIView, CustomListAPIView,
)
from workspace_control.models import WorkspaceModel
from workspace_control.serializers.workspace import WorkspaceModelSerializer


class GetWorkspaceListAPIView(CustomListAPIView):
    queryset = WorkspaceModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = WorkspaceModelSerializer.List
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', ]


class GetWorkspaceDetailsAPIView(CustomRetrieveAPIView):
    queryset = WorkspaceModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = WorkspaceModelSerializer.List

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user

        if not requested_user.check_object_permissions(instance):
            return Response({
                'detail': 'You don\'t have permission to perform this action.'
            }, status=HTTP_403_FORBIDDEN)

        serializer = WorkspaceModelSerializer.List(instance)
        return Response({
            'data': serializer.data,
        }, status=HTTP_200_OK)


class CreateWorkspaceAPIView(CustomCreateAPIView):
    queryset = WorkspaceModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = WorkspaceModelSerializer.Write

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        workspace = WorkspaceModel.objects.create(
            created_by=request.user,
            **validated_data
        )
        workspace.save()

        return Response({
            'message': 'Workspace created successfully.',
        }, status=HTTP_201_CREATED)


class UpdateWorkspaceDetailsAPIView(CustomUpdateAPIView):
    queryset = WorkspaceModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = WorkspaceModelSerializer.Write

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user

        if not requested_user.check_object_permissions(instance):
            return Response({
                'message': 'You don\'t have permission to perform this action.'
            }, status=HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            updated_by=request.user,
        )
        return Response(serializer.data, status=HTTP_200_OK)
