from django.urls import path

from workspace_control.views.project import (
    GetProjectListAPIView, GetProjectDetailsAPIView, CreateProjectAPIView, UpdateProjectDetailsAPIView,
)
from workspace_control.views.workspace import (
    GetWorkspaceListAPIView, GetWorkspaceDetailsAPIView, CreateWorkspaceAPIView, UpdateWorkspaceDetailsAPIView,
)
from workspace_control.views.workspace_member import (
    GetWorkspaceMemberListAPIView, GetWorkspaceMemberDetailsAPIView, CreateWorkspaceMemberAPIView,
    UpdateWorkspaceMemberDetailsAPIView,
)

urlpatterns = [
    path('workspace/list/', GetWorkspaceListAPIView.as_view(), name='workspace-list'),
    path('workspace/create/', CreateWorkspaceAPIView.as_view(), name='workspace-create'),
    path('workspace/<int:pk>/', GetWorkspaceDetailsAPIView.as_view(), name='workspace-detail'),
    path('workspace/<int:pk>/update/', UpdateWorkspaceDetailsAPIView.as_view(), name='workspace-update'),

    path('workspace-member/list/', GetWorkspaceMemberListAPIView.as_view(), name='workspace-member-list'),
    path('workspace-member/create/', CreateWorkspaceMemberAPIView.as_view(), name='workspace-member-create'),
    path('workspace-member/<int:pk>/', GetWorkspaceMemberDetailsAPIView.as_view(), name='workspace-member-detail'),
    path('workspace-member/<int:pk>/update/', UpdateWorkspaceMemberDetailsAPIView.as_view(),
         name='workspace-member-update'),

    path('project/list/', GetProjectListAPIView.as_view(), name='project-list'),
    path('project/create/', CreateProjectAPIView.as_view(), name='project-create'),
    path('project/<str:uuid>/', GetProjectDetailsAPIView.as_view(), name='project-detail'),
    path('project/<int:pk>/update/', UpdateProjectDetailsAPIView.as_view(), name='project-update'),
]
