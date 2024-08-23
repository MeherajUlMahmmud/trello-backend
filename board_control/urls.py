from django.urls import path

from board_control.views.board import (
    GetBoardListAPIView, GetBoardDetailsAPIView, CreateBoardAPIView, UpdateBoardDetailsAPIView,
)
from board_control.views.card import (
    GetCardListAPIView, GetCardDetailsAPIView, CreateCardAPIView, UpdateCardDetailsAPIView,
)
from board_control.views.card_assignment import (
    GetCardAssignmentListAPIView, GetCardAssignmentDetailsAPIView, CreateCardAssignmentAPIView,
    UpdateCardAssignmentDetailsAPIView,
)

urlpatterns = [
    path('boards/list/', GetBoardListAPIView.as_view(), name='board-list'),
    path('boards/<int:pk>/', GetBoardDetailsAPIView.as_view(), name='board-detail'),
    path('boards/create/', CreateBoardAPIView.as_view(), name='board-create'),
    path('boards/<int:pk>/update/',
         UpdateBoardDetailsAPIView.as_view(), name='board-update'),

    path('cards/list/', GetCardListAPIView.as_view(), name='card-list'),
    path('cards/<int:pk>/', GetCardDetailsAPIView.as_view(), name='card-detail'),
    path('cards/create/', CreateCardAPIView.as_view(), name='card-create'),
    path('cards/<int:pk>/update/', UpdateCardDetailsAPIView.as_view(), name='card-update'),

    path('card-assignments/list/', GetCardAssignmentListAPIView.as_view(),
         name='card-assignment-list'),
    path('card-assignments/<int:pk>/',
         GetCardAssignmentDetailsAPIView.as_view(), name='card-assignment-detail'),
    path('card-assignments/create/', CreateCardAssignmentAPIView.as_view(),
         name='card-assignment-create'),
    path('card-assignments/<int:pk>/update/', UpdateCardAssignmentDetailsAPIView.as_view(),
         name='card-assignment-update'),
]
