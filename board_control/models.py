from django.db import models

from common.models import BaseModel
from user_control.models import UserModel
from workspace_control.models import ProjectModel


class BoardModel(BaseModel):
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    serial = models.IntegerField(default=0)

    class Meta:
        db_table = 'board'
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'

    def __str__(self):
        return self.title + ' - ' + self.project.title


class CardModel(BaseModel):
    board = models.ForeignKey(BoardModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    serial = models.IntegerField(default=0)

    class Meta:
        db_table = 'card'
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    def __str__(self):
        return self.title


class CardAssignmentModel(BaseModel):
    card = models.ForeignKey(CardModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'card_assignment'
        verbose_name = 'Card Assignment'
        verbose_name_plural = 'Card Assignments'

    def __str__(self):
        return f'{self.card.title} - {self.user.username}'
