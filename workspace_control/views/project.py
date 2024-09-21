import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from common.custom_view import (
    CustomCreateAPIView, CustomUpdateAPIView, CustomRetrieveAPIView, CustomListAPIView,
)
from common.utils import save_picture_to_folder
from workspace_control.custom_filters import ProjectModelFilter
from workspace_control.models import ProjectModel
from workspace_control.serializers.project import ProjectModelSerializer, BoardOrderSerializer

logger = logging.getLogger(__name__)


class GetProjectListAPIView(CustomListAPIView):
    queryset = ProjectModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProjectModelSerializer.List
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ProjectModelFilter
    search_fields = ['title', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return queryset
            return queryset.filter(created_by=self.request.user)
        else:
            return queryset.none()


class GetProjectDetailsAPIView(CustomRetrieveAPIView):
    queryset = ProjectModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProjectModelSerializer.List
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user

        if not requested_user.check_object_permissions(instance):
            return Response({
                'detail': 'You do not have permission to perform this action'
            }, status=HTTP_403_FORBIDDEN)

        serializer = ProjectModelSerializer.List(instance)
        return Response({
            'data': serializer.data,
        }, status=HTTP_200_OK)


class CreateProjectAPIView(CustomCreateAPIView):
    queryset = ProjectModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProjectModelSerializer.Write

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            project = ProjectModel.objects.create(
                created_by=request.user,
                **validated_data
            )
            project.save()

            return Response({
                'detail': 'Project created successfully.',
            }, status=HTTP_201_CREATED)

        logger.error(serializer.errors)
        # get the first serializer error
        error = next(iter(serializer.errors.values()))[0]
        return Response({
            'detail': error,
        }, status=HTTP_400_BAD_REQUEST)


class UpdateProjectDetailsAPIView(CustomUpdateAPIView):
    queryset = ProjectModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProjectModelSerializer.Write

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user

        if not requested_user.check_object_permissions(instance):
            return Response({
                'detail': 'You don\'t have permission to perform this action.'
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

            project = serializer.save(
                updated_by=request.user,
            )
            serialized_project = ProjectModelSerializer.List(project, many=False)
            return Response({
                'data': serialized_project.data,
            }, status=HTTP_200_OK)

        logger.error(serializer.errors)
        # get the first serializer error
        error = next(iter(serializer.errors.values()))[0]
        return Response({
            'detail': error,
        }, status=HTTP_400_BAD_REQUEST)


class UpdateBoardOrderAPIView(APIView):
    def patch(self, request, uuid):
        data = request.data
        logger.info("data", data)
        serializer = BoardOrderSerializer(
            data=request.data,
            context={'project_uuid': uuid}
        )
        if serializer.is_valid():
            serializer.update(None, serializer.validated_data)
            return Response({
                'detail': 'Board order updated successfully.',
            }, status=HTTP_200_OK)

        logger.error(serializer.errors)
        # get the first serializer error
        error = next(iter(serializer.errors.values()))[0]
        return Response({
            'detail': error,
        }, status=HTTP_400_BAD_REQUEST)
