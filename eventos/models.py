from django.conf import settings
from django.db import models


class TipoEvento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)
    cor = models.CharField(max_length=20, null=True, blank=True)
    icone = models.CharField(max_length=50, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = "tipos_evento"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Evento(models.Model):
    class Escopo(models.TextChoices):
        GERAL = "GERAL", "Geral"
        TURMA = "TURMA", "Turma"

    class Prioridade(models.TextChoices):
        BAIXA = "BAIXA", "Baixa"
        NORMAL = "NORMAL", "Normal"
        ALTA = "ALTA", "Alta"
        URGENTE = "URGENTE", "Urgente"

    class Publico(models.TextChoices):
        PAIS = "PAIS", "Pais"
        PROFESSORES = "PROFESSORES", "Professores"
        TODOS = "TODOS", "Todos"

    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fim = models.TimeField(null=True, blank=True)
    tipo_evento = models.ForeignKey(
        "eventos.TipoEvento",
        on_delete=models.RESTRICT,
        db_column="tipo_evento_id",
        related_name="eventos",
        db_index=False,
    )
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column="criado_por",
        related_name="eventos_criados",
    )
    escopo = models.CharField(max_length=5, choices=Escopo.choices, default=Escopo.GERAL)
    prioridade = models.CharField(max_length=7, choices=Prioridade.choices, default=Prioridade.NORMAL)
    local_evento = models.CharField(max_length=150, null=True, blank=True)
    publico = models.CharField(max_length=11, choices=Publico.choices, default=Publico.TODOS)
    publicado = models.BooleanField(default=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    turmas = models.ManyToManyField("turmas.Turma", through="eventos.EventoTurma", related_name="eventos", blank=True)

    class Meta:
        db_table = "eventos"
        indexes = [
            models.Index(fields=["data_inicio"], name="idx_eventos_data_inicio"),
            models.Index(fields=["tipo_evento"], name="idx_eventos_tipo"),
            models.Index(fields=["publicado"], name="idx_eventos_publicado"),
        ]
        ordering = ["data_inicio", "hora_inicio"]

    def __str__(self):
        return self.titulo


class EventoTurma(models.Model):
    id = models.BigAutoField(primary_key=True)
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        db_column="evento_id",
        related_name="eventos_turmas",
    )
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.CASCADE,
        db_column="turma_id",
        related_name="eventos_turmas",
    )

    class Meta:
        db_table = "eventos_turmas"
        constraints = [
            models.UniqueConstraint(fields=["evento", "turma"], name="uq_evento_turma"),
        ]

    def __str__(self):
        return f"{self.evento.titulo} -> {self.turma.nome_turma}"

