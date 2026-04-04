from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.permissions import PapelRequiredMixin

from .forms import AvisoForm
from .models import Aviso
from .services import avisos_visiveis_para_usuario


class GestorRequiredMixin(PapelRequiredMixin):
    papeis_permitidos = ("ADMIN", "DIRETOR", "PROFESSOR")


class AvisoListView(LoginRequiredMixin, ListView):
    model = Aviso
    template_name = "avisos/aviso_list.html"
    context_object_name = "avisos"
    paginate_by = 10

    def get_queryset(self):
        return avisos_visiveis_para_usuario(self.request.user)


class AvisoDetailView(LoginRequiredMixin, DetailView):
    model = Aviso
    template_name = "avisos/aviso_detail.html"
    context_object_name = "aviso"

    def get_queryset(self):
        return avisos_visiveis_para_usuario(self.request.user)


class AvisoCreateView(GestorRequiredMixin, CreateView):
    model = Aviso
    form_class = AvisoForm
    template_name = "avisos/aviso_form.html"
    success_url = reverse_lazy("avisos:lista")

    def form_valid(self, form):
        form.instance.publicado_por = self.request.user
        messages.success(self.request, "Aviso cadastrado com sucesso.")
        return super().form_valid(form)


class AvisoUpdateView(GestorRequiredMixin, UpdateView):
    model = Aviso
    form_class = AvisoForm
    template_name = "avisos/aviso_form.html"
    success_url = reverse_lazy("avisos:lista")

    def form_valid(self, form):
        messages.success(self.request, "Aviso atualizado com sucesso.")
        return super().form_valid(form)


class AvisoDeleteView(GestorRequiredMixin, DeleteView):
    model = Aviso
    template_name = "avisos/aviso_confirm_delete.html"
    success_url = reverse_lazy("avisos:lista")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Aviso removido com sucesso.")
        return super().delete(request, *args, **kwargs)

