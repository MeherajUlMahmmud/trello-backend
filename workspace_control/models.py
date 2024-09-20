from django.db import models

from common.choices import WorkspaceRoleChoices
from common.models import BaseModel
from common.utils import generate_uuid
from user_control.models import UserModel


class WorkspaceModel(BaseModel):
    uuid = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'workspace'
        verbose_name = 'Workspace'
        verbose_name_plural = 'Workspaces'

        ordering = ['created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.uuid:
            uuid = generate_uuid()
            exists = WorkspaceModel.objects.filter(uuid=uuid).exists()
            while exists:
                uuid = generate_uuid()
                exists = WorkspaceModel.objects.filter(uuid=uuid).exists()
            self.uuid = uuid

        return super().save(*args, **kwargs)


class WorkspaceMemberModel(BaseModel):
    workspace = models.ForeignKey(WorkspaceModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=WorkspaceRoleChoices.choices, default=WorkspaceRoleChoices.MEMBER)

    class Meta:
        db_table = 'workspace_member'
        verbose_name = 'Workspace Member'
        verbose_name_plural = 'Workspace Members'

        ordering = ['created_at']

    def __str__(self):
        return f'{self.workspace.title} - {self.user.email}'


class ProjectModel(BaseModel):
    uuid = models.CharField(max_length=255, unique=True)
    workspace = models.ForeignKey(WorkspaceModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'project'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

        ordering = ['created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.uuid:
            project_uuid = generate_uuid()
            exists = ProjectModel.objects.filter(uuid=project_uuid).exists()
            while exists:
                project_uuid = generate_uuid()
                exists = ProjectModel.objects.filter(uuid=project_uuid).exists()
            self.uuid = project_uuid

        return super().save(*args, **kwargs)
