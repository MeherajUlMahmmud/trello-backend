from django.db import models

YesNoChoices = [
    (None, 'All'),
    (True, 'Yes'),
    (False, 'No'),
]


class WorkspaceRoleChoices(models.TextChoices):
    OWNER = 'Owner', 'Owner'
    MEMBER = 'Member', 'Member'
