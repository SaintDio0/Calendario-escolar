from django.contrib import admin

from .models import Aluno, AnoLetivo, Turma


@admin.register(AnoLetivo)
class AnoLetivoAdmin(admin.ModelAdmin):
    list_display = ("ano", "ativo", "data_criacao")
    list_filter = ("ativo",)
    search_fields = ("ano",)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("nome_turma", "serie", "segmento", "turno", "ano_letivo", "ativo")
    list_filter = ("ano_letivo", "segmento", "turno", "ativo")
    search_fields = ("nome_turma", "serie")


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("nome", "matricula", "turma", "ativo")
    list_filter = ("turma", "ativo")
    search_fields = ("nome", "matricula")

