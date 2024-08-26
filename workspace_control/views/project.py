from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from common.custom_view import (
    CustomCreateAPIView, CustomUpdateAPIView, CustomRetrieveAPIView, CustomListAPIView,
)
from workspace_control.custom_filters import ProjectModelFilter
from workspace_control.models import ProjectModel
from workspace_control.serializers.project import ProjectModelSerializer


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
        return Response(serializer.data, status=HTTP_200_OK)


class CreateProjectAPIView(CustomCreateAPIView):
    queryset = ProjectModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProjectModelSerializer.Write

    def post(self, request, *args, **kwargs):
        print(f'data: {request.data}')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        project = ProjectModel.objects.create(
            created_by=request.user,
            **validated_data
        )
        project.save()

        return Response({
            'message': 'Project created successfully.',
        }, status=HTTP_201_CREATED)


class UpdateProjectDetailsAPIView(CustomUpdateAPIView):
    queryset = ProjectModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProjectModelSerializer.Write

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
