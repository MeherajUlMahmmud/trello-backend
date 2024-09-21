import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from common.custom_view import (
    CustomCreateAPIView, CustomUpdateAPIView, CustomRetrieveAPIView, CustomListAPIView,
)
from common.utils import save_picture_to_folder
from workspace_control.models import WorkspaceModel
from workspace_control.serializers.workspace import WorkspaceModelSerializer

logger = logging.getLogger(__name__)


class GetWorkspaceListAPIView(CustomListAPIView):
    queryset = WorkspaceModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = WorkspaceModelSerializer.List
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return queryset
            return queryset.filter(created_by=self.request.user)
        else:
            return queryset.none()


class GetWorkspaceDetailsAPIView(CustomRetrieveAPIView):
    queryset = WorkspaceModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = WorkspaceModelSerializer.List

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user

        if not requested_user.check_object_permissions(instance):
            return Response({
                'detail': 'You do not have permission to perform this action'
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
        if serializer.is_valid():
            validated_data = serializer.validated_data

            image = request.FILES.get('image')
            if image is not None:
                image_path = save_picture_to_folder(image, 'workspace_images')
                serializer.validated_data['image'] = image_path

            workspace = WorkspaceModel.objects.create(
                created_by=request.user,
                **validated_data
            )
            workspace.save()

            return Response({
                'detail': 'Workspace created successfully.',
            }, status=HTTP_201_CREATED)

        logger.error(serializer.errors)
        # get the first serializer error
        error = next(iter(serializer.errors.values()))[0]
        return Response({
            'detail': error,
        }, status=HTTP_400_BAD_REQUEST)


class UpdateWorkspaceDetailsAPIView(CustomUpdateAPIView):
    queryset = WorkspaceModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = WorkspaceModelSerializer.Write

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user

        if not requested_user.check_object_permissions(instance):
            return Response({
                'detail': 'You do not have permission to perform this action.'
            }, status=HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(
            instance,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            image = request.FILES.get('image')
            if image is not None:
                image_path = save_picture_to_folder(image, 'workspace_images')
                serializer.validated_data['image'] = image_path

            workspace = serializer.save(
                updated_by=request.user,
            )
            serialized_workspace = WorkspaceModelSerializer.List(workspace, many=False)
            return Response({
                'data': serialized_workspace.data,
            }, status=HTTP_200_OK)

        logger.error(serializer.errors)
        # get the first serializer error
        error = next(iter(serializer.errors.values()))[0]
        return Response({
            'detail': error,
        }, status=HTTP_400_BAD_REQUEST)
