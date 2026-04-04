from django.urls import path

from .views import AvisoCreateView, AvisoDeleteView, AvisoDetailView, AvisoListView, AvisoUpdateView

app_name = "avisos"

urlpatterns = [
    path("", AvisoListView.as_view(), name="lista"),
    path("novo/", AvisoCreateView.as_view(), name="novo"),
    path("<int:pk>/", AvisoDetailView.as_view(), name="detalhe"),
    path("<int:pk>/editar/", AvisoUpdateView.as_view(), name="editar"),
    path("<int:pk>/excluir/", AvisoDeleteView.as_view(), name="excluir"),
]

