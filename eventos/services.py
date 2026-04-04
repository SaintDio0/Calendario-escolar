from django.db.models import Q

from turmas.models import Turma
from usuarios.models import ResponsavelAluno

from .models import Evento


def turmas_do_responsavel(usuario):
    return Turma.objects.filter(alunos__responsaveis__usuario=usuario).distinct()


def eventos_visiveis_para_usuario(usuario):
    qs = Evento.objects.filter(ativo=True, publicado=True).select_related("tipo_evento", "criado_por").prefetch_related("turmas")

    if not getattr(usuario, "is_authenticated", False):
        return qs.none()

    if usuario.tipo_usuario in {"ADMIN", "DIRETOR", "PROFESSOR"}:
        return Evento.objects.filter(ativo=True).select_related("tipo_evento", "criado_por").prefetch_related("turmas")

    if usuario.tipo_usuario == "RESPONSAVEL":
        ids_turmas = ResponsavelAluno.objects.filter(usuario=usuario).values_list("aluno__turma_id", flat=True)
        return qs.filter(
            Q(escopo=Evento.Escopo.GERAL)
            | Q(eventos_turmas__turma_id__in=ids_turmas)
        ).filter(
            Q(publico=Evento.Publico.PAIS) | Q(publico=Evento.Publico.TODOS)
        ).distinct()

    return qs.none()


def aplicar_filtros_eventos(queryset, dados):
    tipo_evento = dados.get("tipo_evento")
    turma = dados.get("turma")
    mes = dados.get("mes")

    if tipo_evento:
        queryset = queryset.filter(tipo_evento=tipo_evento)

    if turma:
        queryset = queryset.filter(Q(escopo=Evento.Escopo.GERAL) | Q(eventos_turmas__turma=turma)).distinct()

    if mes:
        try:
            ano, numero_mes = mes.split("-")
            queryset = queryset.filter(data_inicio__year=int(ano), data_inicio__month=int(numero_mes))
        except ValueError:
            pass

    return queryset
