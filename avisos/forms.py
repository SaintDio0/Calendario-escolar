from django import forms

from turmas.models import Turma

from .models import Aviso, AvisoTurma


class AvisoForm(forms.ModelForm):
    turmas = forms.ModelMultipleChoiceField(
        queryset=Turma.objects.filter(ativo=True),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        help_text="Selecione turmas quando o escopo for TURMA.",
    )

    class Meta:
        model = Aviso
        fields = ["titulo", "mensagem", "data_expiracao", "escopo", "ativo", "turmas"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "mensagem": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "data_expiracao": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "escopo": forms.Select(attrs={"class": "form-select"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["turmas"].initial = self.instance.turmas.all()

    def clean(self):
        cleaned_data = super().clean()
        escopo = cleaned_data.get("escopo")
        turmas = cleaned_data.get("turmas")
        if escopo == Aviso.Escopo.TURMA and (not turmas or turmas.count() == 0):
            self.add_error("turmas", "Selecione ao menos uma turma para aviso de escopo TURMA.")
        return cleaned_data

    def save(self, commit=True):
        aviso = super().save(commit=commit)
        if commit:
            AvisoTurma.objects.filter(aviso=aviso).delete()
            if self.cleaned_data.get("escopo") == Aviso.Escopo.TURMA:
                for turma in self.cleaned_data.get("turmas", []):
                    AvisoTurma.objects.get_or_create(aviso=aviso, turma=turma)
        return aviso

