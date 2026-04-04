from django.contrib import admin

from .models import LogSistema


@admin.register(LogSistema)
class LogSistemaAdmin(admin.ModelAdmin):
    list_display = ("acao", "usuario", "tabela_afetada", "registro_id", "data_acao")
    list_filter = ("acao", "tabela_afetada", "data_acao")
    search_fields = ("descricao", "ip_origem")

