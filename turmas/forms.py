from django import forms

from usuarios.models import ResponsavelAluno, Usuario

from .models import Aluno, Turma


class AlunoCadastroForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome", "data_nascimento", "matricula", "turma", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome completo do aluno"}),
            "data_nascimento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "matricula": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: MAT2026003"}),
            "turma": forms.Select(attrs={"class": "form-select"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["turma"].queryset = Turma.objects.filter(ativo=True)


class ResponsavelCadastroForm(forms.ModelForm):
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mínimo 6 caracteres"}),
        min_length=6,
    )
    confirmar_senha = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repita a senha"}),
        min_length=6,
    )

    class Meta:
        model = Usuario
        fields = ["nome", "email", "telefone", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome do responsável"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@dominio.com"}),
            "telefone": forms.TextInput(attrs={"class": "form-control", "placeholder": "(17)99999-0004"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")
        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error("confirmar_senha", "As senhas não conferem.")
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.tipo_usuario = Usuario.TipoUsuario.RESPONSAVEL
        usuario.is_staff = False
        usuario.is_superuser = False
        usuario.set_password(self.cleaned_data["senha"])
        if commit:
            usuario.save()
        return usuario


class ResponsavelAlunoForm(forms.ModelForm):
    class Meta:
        model = ResponsavelAluno
        fields = ["usuario", "aluno", "parentesco", "responsavel_principal"]
        widgets = {
            "usuario": forms.Select(attrs={"class": "form-select"}),
            "aluno": forms.Select(attrs={"class": "form-select"}),
            "parentesco": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: Mãe"}),
            "responsavel_principal": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["usuario"].queryset = Usuario.objects.filter(tipo_usuario=Usuario.TipoUsuario.RESPONSAVEL, ativo=True)
