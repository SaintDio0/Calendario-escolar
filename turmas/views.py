from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from core.permissions import PapelRequiredMixin, usuario_e_gestor
from usuarios.models import ResponsavelAluno

from .forms import AlunoCadastroForm, ResponsavelAlunoForm, ResponsavelCadastroForm
from .models import Aluno, Turma


class DiretorCadastroMixin(PapelRequiredMixin):
    papeis_permitidos = ("DIRETOR", "ADMIN")


class TurmaListView(ListView):
    model = Turma
    template_name = "turmas/turma_list.html"
    context_object_name = "turmas"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("usuarios:login")
        if not usuario_e_gestor(request.user):
            messages.error(request, "Você não tem permissão para acessar esta área.")
            return redirect("core:dashboard_router")
        return super().dispatch(request, *args, **kwargs)


class AlunoListView(ListView):
    model = Aluno
    template_name = "turmas/aluno_list.html"
    context_object_name = "alunos"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("usuarios:login")
        if not usuario_e_gestor(request.user):
            messages.error(request, "Você não tem permissão para acessar esta área.")
            return redirect("core:dashboard_router")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Aluno.objects.select_related("turma", "turma__ano_letivo")
        turma_id = self.request.GET.get("turma")
        if turma_id:
            qs = qs.filter(turma_id=turma_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["turmas_filtro"] = Turma.objects.all()
        context["turma_selecionada"] = self.request.GET.get("turma", "")
        return context


class AlunoCreateView(DiretorCadastroMixin, CreateView):
    model = Aluno
    form_class = AlunoCadastroForm
    template_name = "turmas/aluno_form.html"
    success_url = reverse_lazy("turmas:alunos")

    def form_valid(self, form):
        messages.success(self.request, "Aluno cadastrado com sucesso.")
        return super().form_valid(form)


class ResponsavelCreateView(DiretorCadastroMixin, CreateView):
    form_class = ResponsavelCadastroForm
    template_name = "turmas/responsavel_form.html"
    success_url = reverse_lazy("turmas:vinculos")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Responsável cadastrado com sucesso. Agora vincule ao aluno.")
        return response


@login_required
def vincular_responsavel_view(request):
    if request.user.tipo_usuario not in {"ADMIN", "DIRETOR"}:
        messages.error(request, "Você não tem permissão para acessar esta área.")
        return redirect("core:dashboard_router")

    form = ResponsavelAlunoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Vínculo criado com sucesso.")
        return redirect("turmas:vinculos")

    vinculos_qs = ResponsavelAluno.objects.select_related("usuario", "aluno", "aluno__turma").order_by("-data_criacao")
    paginator = Paginator(vinculos_qs, 10)
    pagina = request.GET.get("page")

    return render(
        request,
        "turmas/vinculos.html",
        {
            "form": form,
            "vinculos": paginator.get_page(pagina),
        },
    )
