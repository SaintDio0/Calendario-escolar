from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UsuarioChangeForm, UsuarioCreationForm
from .models import ResponsavelAluno, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = Usuario

    list_display = ("nome", "email", "tipo_usuario", "ativo", "is_staff")
    list_filter = ("tipo_usuario", "ativo", "is_staff")
    ordering = ("nome",)
    search_fields = ("nome", "email", "telefone")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Dados pessoais", {"fields": ("nome", "telefone", "tipo_usuario")}),
        ("Permissões", {"fields": ("ativo", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas", {"fields": ("last_login", "data_criacao", "data_atualizacao")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("nome", "email", "tipo_usuario", "telefone", "password1", "password2", "ativo"),
            },
        ),
    )

    readonly_fields = ("last_login", "data_criacao", "data_atualizacao")


@admin.register(ResponsavelAluno)
class ResponsavelAlunoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "aluno", "parentesco", "responsavel_principal", "data_criacao")
    list_filter = ("responsavel_principal",)
    search_fields = ("usuario__nome", "aluno__nome", "aluno__matricula")

