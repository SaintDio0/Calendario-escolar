from django.db.models import Q

from usuarios.models import ResponsavelAluno

from .models import Aviso


def avisos_visiveis_para_usuario(usuario):
    qs = Aviso.objects.filter(ativo=True).select_related("publicado_por").prefetch_related("turmas")

    if not getattr(usuario, "is_authenticated", False):
        return qs.none()

    if usuario.tipo_usuario in {"ADMIN", "DIRETOR", "PROFESSOR"}:
        return qs

    if usuario.tipo_usuario == "RESPONSAVEL":
        ids_turma = ResponsavelAluno.objects.filter(usuario=usuario).values_list("aluno__turma_id", flat=True)
        return qs.filter(Q(escopo=Aviso.Escopo.GERAL) | Q(avisos_turmas__turma_id__in=ids_turma)).distinct()

    return qs.none()

