from django.contrib import admin

from .models import Evento, EventoTurma, TipoEvento


@admin.register(TipoEvento)
class TipoEventoAdmin(admin.ModelAdmin):
    list_display = ("nome", "cor", "icone", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome",)


class EventoTurmaInline(admin.TabularInline):
    model = EventoTurma
    extra = 1


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo_evento", "data_inicio", "escopo", "prioridade", "publicado", "ativo")
    list_filter = ("tipo_evento", "escopo", "prioridade", "publicado", "ativo")
    search_fields = ("titulo", "descricao", "local_evento")
    inlines = [EventoTurmaInline]


@admin.register(EventoTurma)
class EventoTurmaAdmin(admin.ModelAdmin):
    list_display = ("evento", "turma")
    search_fields = ("evento__titulo", "turma__nome_turma")

