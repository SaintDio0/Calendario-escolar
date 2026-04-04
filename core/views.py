from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View

from avisos.services import avisos_visiveis_para_usuario
from core.permissions import usuario_e_gestor, usuario_e_responsavel
from eventos.services import eventos_visiveis_para_usuario
from turmas.models import Aluno


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:dashboard_router")
        return redirect("usuarios:login")


class DashboardRouterView(LoginRequiredMixin, View):
    def get(self, request):
        if usuario_e_responsavel(request.user):
            return redirect("core:dashboard_responsavel")
        return redirect("core:dashboard_gestor")


class DashboardGestorView(LoginRequiredMixin, View):
    template_name = "core/dashboard_gestor.html"

    def get(self, request):
        if not usuario_e_gestor(request.user):
            return redirect("core:dashboard_responsavel")

        hoje = timezone.now().date()
        inicio_mes = hoje.replace(day=1)

        eventos_qs = eventos_visiveis_para_usuario(request.user)
        avisos_qs = avisos_visiveis_para_usuario(request.user)

        contexto = {
            "total_eventos": eventos_qs.count(),
            "eventos_mes": eventos_qs.filter(data_inicio__gte=inicio_mes).count(),
            "eventos_hoje": eventos_qs.filter(data_inicio=hoje).count(),
            "proximos_eventos": eventos_qs.filter(data_inicio__gte=hoje)[:6],
            "avisos_ativos": avisos_qs.count(),
            "proximos_avisos": avisos_qs[:5],
        }
        return render(request, self.template_name, contexto)


class DashboardResponsavelView(LoginRequiredMixin, View):
    template_name = "core/dashboard_responsavel.html"

    def get(self, request):
        if not usuario_e_responsavel(request.user):
            return redirect("core:dashboard_gestor")

        hoje = timezone.now().date()
        alunos = Aluno.objects.filter(responsaveis__usuario=request.user).distinct()
        eventos_qs = eventos_visiveis_para_usuario(request.user)
        avisos_qs = avisos_visiveis_para_usuario(request.user)

        contexto = {
            "alunos": alunos,
            "total_alunos": alunos.count(),
            "eventos_hoje": eventos_qs.filter(data_inicio=hoje).count(),
            "proximos_eventos": eventos_qs.filter(data_inicio__gte=hoje)[:8],
            "avisos": avisos_qs[:6],
        }
        return render(request, self.template_name, contexto)

