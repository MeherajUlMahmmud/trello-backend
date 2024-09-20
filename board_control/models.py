from django.db import models
import uuid

from common.models import BaseModel
from user_control.models import UserModel
from workspace_control.models import ProjectModel


class BoardModel(BaseModel):
    uuid = models.CharField(max_length=255, unique=True)
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

    def save(self, *args, **kwargs):
        # Generate a UUID if not present
        if not self.uuid:
            board_uuid = uuid.uuid4()
            exists = BoardModel.objects.filter(uuid=board_uuid).exists()
            while exists:
                board_uuid = uuid.uuid4()
                exists = BoardModel.objects.filter(uuid=board_uuid).exists()
            self.uuid = board_uuid

        # Set the serial to the highest existing serial + 1 within the same board
        if self.serial == 0:
            max_serial = BoardModel.objects.filter(project=self.project).aggregate(max_serial=models.Max('serial'))[
                'max_serial']
            self.serial = (max_serial or 0) + 1

        return super().save(*args, **kwargs)


class CardModel(BaseModel):
    uuid = models.CharField(max_length=255, unique=True)
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

    def save(self, *args, **kwargs):
        # Generate a UUID if not present
        if not self.uuid:
            card_uuid = uuid.uuid4()
            exists = CardModel.objects.filter(uuid=card_uuid).exists()
            while exists:
                card_uuid = uuid.uuid4()
                exists = CardModel.objects.filter(uuid=card_uuid).exists()
            self.uuid = card_uuid

        # Set the serial to the highest existing serial + 1 within the same board
        if self.serial == 0:
            max_serial = CardModel.objects.filter(board=self.board).aggregate(max_serial=models.Max('serial'))[
                'max_serial']
            self.serial = (max_serial or 0) + 1

        return super().save(*args, **kwargs)


class CardAssignmentModel(BaseModel):
    card = models.ForeignKey(CardModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'card_assignment'
        verbose_name = 'Card Assignment'
        verbose_name_plural = 'Card Assignments'

    def __str__(self):
        return f'{self.card.title} - {self.user.username}'
