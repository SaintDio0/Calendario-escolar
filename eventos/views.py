from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from core.permissions import PapelRequiredMixin
from turmas.models import Turma

from .forms import EventoFiltroForm, EventoForm
from .models import Evento, TipoEvento
from .services import aplicar_filtros_eventos, eventos_visiveis_para_usuario, turmas_do_responsavel


class GestorRequiredMixin(PapelRequiredMixin):
    papeis_permitidos = ("ADMIN", "DIRETOR", "PROFESSOR")


class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = "eventos/evento_list.html"
    context_object_name = "eventos"
    paginate_by = 10

    def get_queryset(self):
        self.filtro_form = EventoFiltroForm(self.request.GET or None)
        queryset = eventos_visiveis_para_usuario(self.request.user)
        if self.filtro_form.is_valid():
            queryset = aplicar_filtros_eventos(queryset, self.filtro_form.cleaned_data)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro_form"] = self.filtro_form
        return context


class EventoDetailView(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = "eventos/evento_detail.html"
    context_object_name = "evento"

    def get_queryset(self):
        return eventos_visiveis_para_usuario(self.request.user)


class EventoCreateView(GestorRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = "eventos/evento_form.html"
    success_url = reverse_lazy("eventos:lista")

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, "Evento cadastrado com sucesso.")
        return super().form_valid(form)


class EventoUpdateView(GestorRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = "eventos/evento_form.html"
    success_url = reverse_lazy("eventos:lista")

    def form_valid(self, form):
        messages.success(self.request, "Evento atualizado com sucesso.")
        return super().form_valid(form)


class EventoDeleteView(GestorRequiredMixin, DeleteView):
    model = Evento
    template_name = "eventos/evento_confirm_delete.html"
    success_url = reverse_lazy("eventos:lista")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Evento excluído com sucesso.")
        return super().delete(request, *args, **kwargs)


class CalendarioView(LoginRequiredMixin, TemplateView):
    template_name = "eventos/calendario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tipos_evento"] = TipoEvento.objects.filter(ativo=True)
        if self.request.user.tipo_usuario == "RESPONSAVEL":
            context["turmas"] = turmas_do_responsavel(self.request.user)
        else:
            context["turmas"] = Turma.objects.filter(ativo=True)
        return context


class CalendarioDataView(LoginRequiredMixin, View):
    def get(self, request):
        queryset = eventos_visiveis_para_usuario(request.user)

        filtro_form = EventoFiltroForm(request.GET)
        if filtro_form.is_valid():
            queryset = aplicar_filtros_eventos(queryset, filtro_form.cleaned_data)

        start = request.GET.get("start")
        end = request.GET.get("end")
        if start and end:
            try:
                start_data = datetime.fromisoformat(start.replace("Z", "")).date()
                end_data = datetime.fromisoformat(end.replace("Z", "")).date()
                queryset = queryset.filter(data_inicio__gte=start_data, data_inicio__lte=end_data)
            except ValueError:
                pass

        eventos_json = []
        for evento in queryset.distinct():
            inicio = datetime.combine(evento.data_inicio, evento.hora_inicio) if evento.hora_inicio else evento.data_inicio.isoformat()
            if evento.data_fim:
                fim = datetime.combine(evento.data_fim, evento.hora_fim) if evento.hora_fim else evento.data_fim.isoformat()
            else:
                fim = None

            eventos_json.append(
                {
                    "id": evento.id,
                    "title": evento.titulo,
                    "start": inicio.isoformat() if hasattr(inicio, "isoformat") else inicio,
                    "end": fim.isoformat() if hasattr(fim, "isoformat") else fim,
                    "color": evento.tipo_evento.cor or "#2563eb",
                    "url": reverse_lazy("eventos:detalhe", kwargs={"pk": evento.id}),
                    "extendedProps": {
                        "tipo": evento.tipo_evento.nome,
                        "prioridade": evento.get_prioridade_display(),
                        "publico": evento.get_publico_display(),
                    },
                }
            )

        return JsonResponse(eventos_json, safe=False)

