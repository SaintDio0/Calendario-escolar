from django import forms

from turmas.models import Turma

from .models import Evento, EventoTurma, TipoEvento


def _bootstrapify(form):
    for field in form.fields.values():
        if isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.setdefault("class", "form-check-input")
        else:
            field.widget.attrs.setdefault("class", "form-control")


class EventoForm(forms.ModelForm):
    turmas = forms.ModelMultipleChoiceField(
        queryset=Turma.objects.filter(ativo=True),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        help_text="Selecione turmas apenas quando o escopo for TURMA.",
    )

    class Meta:
        model = Evento
        fields = [
            "titulo",
            "descricao",
            "data_inicio",
            "data_fim",
            "hora_inicio",
            "hora_fim",
            "tipo_evento",
            "escopo",
            "prioridade",
            "local_evento",
            "publico",
            "publicado",
            "ativo",
            "turmas",
        ]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3}),
            "data_inicio": forms.DateInput(attrs={"type": "date"}),
            "data_fim": forms.DateInput(attrs={"type": "date"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time"}),
            "hora_fim": forms.TimeInput(attrs={"type": "time"}),
            "tipo_evento": forms.Select(attrs={"class": "form-select"}),
            "escopo": forms.Select(attrs={"class": "form-select"}),
            "prioridade": forms.Select(attrs={"class": "form-select"}),
            "publico": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrapify(self)
        self.fields["tipo_evento"].queryset = TipoEvento.objects.filter(ativo=True)
        if self.instance.pk:
            self.fields["turmas"].initial = self.instance.turmas.all()

    def clean(self):
        cleaned_data = super().clean()
        escopo = cleaned_data.get("escopo")
        turmas = cleaned_data.get("turmas")

        if escopo == Evento.Escopo.TURMA and (not turmas or turmas.count() == 0):
            self.add_error("turmas", "Selecione ao menos uma turma para evento de escopo TURMA.")

        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")
        if data_inicio and data_fim and data_fim < data_inicio:
            self.add_error("data_fim", "Data final não pode ser anterior à data inicial.")

        return cleaned_data

    def save(self, commit=True):
        evento = super().save(commit=commit)
        if commit:
            EventoTurma.objects.filter(evento=evento).delete()
            if self.cleaned_data.get("escopo") == Evento.Escopo.TURMA:
                for turma in self.cleaned_data.get("turmas", []):
                    EventoTurma.objects.get_or_create(evento=evento, turma=turma)
        return evento


class EventoFiltroForm(forms.Form):
    tipo_evento = forms.ModelChoiceField(
        queryset=TipoEvento.objects.filter(ativo=True),
        required=False,
        empty_label="Todos os tipos",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    turma = forms.ModelChoiceField(
        queryset=Turma.objects.filter(ativo=True),
        required=False,
        empty_label="Todas as turmas",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    mes = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "type": "month"}))

