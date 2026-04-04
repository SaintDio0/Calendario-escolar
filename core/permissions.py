from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.shortcuts import redirect


class PapelRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    papeis_permitidos = ()
    mensagem_sem_permissao = "Você não tem permissão para acessar esta área."

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.tipo_usuario in self.papeis_permitidos

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())
        messages.error(self.request, self.mensagem_sem_permissao)
        return redirect("core:dashboard_router")


def usuario_e_gestor(user):
    if not getattr(user, "is_authenticated", False):
        return False
    return user.tipo_usuario in {"ADMIN", "DIRETOR", "PROFESSOR"}


def usuario_e_responsavel(user):
    if not getattr(user, "is_authenticated", False):
        return False
    return user.tipo_usuario == "RESPONSAVEL"

