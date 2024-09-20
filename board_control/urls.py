from django.urls import path

from board_control.views.board import (
    GetBoardListAPIView, GetBoardDetailsAPIView, CreateBoardAPIView, UpdateBoardDetailsAPIView, UpdateCardOrderAPIView,
)
from board_control.views.card import (
    GetCardListAPIView, GetCardDetailsAPIView, CreateCardAPIView, UpdateCardDetailsAPIView,
)
from board_control.views.card_assignment import (
    GetCardAssignmentListAPIView, GetCardAssignmentDetailsAPIView, CreateCardAssignmentAPIView,
    UpdateCardAssignmentDetailsAPIView,
)

urlpatterns = [
    path('board/list/', GetBoardListAPIView.as_view(), name='board-list'),
    path('board/<int:pk>/', GetBoardDetailsAPIView.as_view(), name='board-detail'),
    path('board/create/', CreateBoardAPIView.as_view(), name='board-create'),
    path('board/<int:pk>/update/', UpdateBoardDetailsAPIView.as_view(), name='board-update'),
    path('board/<str:uuid>/update-board-order/', UpdateCardOrderAPIView.as_view(), name='update-card-order'),

    path('card/list/', GetCardListAPIView.as_view(), name='card-list'),
    path('card/<int:pk>/', GetCardDetailsAPIView.as_view(), name='card-detail'),
    path('card/create/', CreateCardAPIView.as_view(), name='card-create'),
    path('card/<int:pk>/update/', UpdateCardDetailsAPIView.as_view(), name='card-update'),

    path('card-assignment/list/', GetCardAssignmentListAPIView.as_view(),
         name='card-assignment-list'),
    path('card-assignment/<int:pk>/',
         GetCardAssignmentDetailsAPIView.as_view(), name='card-assignment-detail'),
    path('card-assignment/create/', CreateCardAssignmentAPIView.as_view(),
         name='card-assignment-create'),
    path('card-assignment/<int:pk>/update/', UpdateCardAssignmentDetailsAPIView.as_view(),
         name='card-assignment-update'),
]
