from django.urls import path

from .views import (
    CalendarioDataView,
    CalendarioView,
    EventoCreateView,
    EventoDeleteView,
    EventoDetailView,
    EventoListView,
    EventoUpdateView,
)

app_name = "eventos"

urlpatterns = [
    path("", EventoListView.as_view(), name="lista"),
    path("calendario/", CalendarioView.as_view(), name="calendario"),
    path("calendario/dados/", CalendarioDataView.as_view(), name="calendario_dados"),
    path("novo/", EventoCreateView.as_view(), name="novo"),
    path("<int:pk>/", EventoDetailView.as_view(), name="detalhe"),
    path("<int:pk>/editar/", EventoUpdateView.as_view(), name="editar"),
    path("<int:pk>/excluir/", EventoDeleteView.as_view(), name="excluir"),
]

