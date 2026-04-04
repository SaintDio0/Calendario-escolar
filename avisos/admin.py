from django.contrib import admin

from .models import Aviso, AvisoTurma


class AvisoTurmaInline(admin.TabularInline):
    model = AvisoTurma
    extra = 1


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "publicado_por", "escopo", "ativo", "data_publicacao")
    list_filter = ("escopo", "ativo", "data_publicacao")
    search_fields = ("titulo", "mensagem")
    inlines = [AvisoTurmaInline]


@admin.register(AvisoTurma)
class AvisoTurmaAdmin(admin.ModelAdmin):
    list_display = ("aviso", "turma")
    search_fields = ("aviso__titulo", "turma__nome_turma")

