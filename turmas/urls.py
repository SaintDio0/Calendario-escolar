from django.urls import path

from .views import (
    AlunoCreateView,
    AlunoListView,
    ResponsavelCreateView,
    TurmaListView,
    vincular_responsavel_view,
)

app_name = "turmas"

urlpatterns = [
    path("", TurmaListView.as_view(), name="lista"),
    path("alunos/", AlunoListView.as_view(), name="alunos"),
    path("alunos/novo/", AlunoCreateView.as_view(), name="aluno_novo"),
    path("responsaveis/novo/", ResponsavelCreateView.as_view(), name="responsavel_novo"),
    path("vinculos/", vincular_responsavel_view, name="vinculos"),
]
