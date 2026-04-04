from django.conf import settings
from django.db import models


class Aviso(models.Model):
    class Escopo(models.TextChoices):
        GERAL = "GERAL", "Geral"
        TURMA = "TURMA", "Turma"

    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    publicado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column="publicado_por",
        related_name="avisos_publicados",
    )
    data_publicacao = models.DateTimeField(auto_now_add=True)
    data_expiracao = models.DateTimeField(null=True, blank=True)
    escopo = models.CharField(max_length=5, choices=Escopo.choices, default=Escopo.GERAL)
    ativo = models.BooleanField(default=True)
    turmas = models.ManyToManyField("turmas.Turma", through="avisos.AvisoTurma", related_name="avisos", blank=True)

    class Meta:
        db_table = "avisos"
        indexes = [
            models.Index(fields=["data_publicacao"], name="idx_avisos_publicacao"),
        ]
        ordering = ["-data_publicacao"]

    def __str__(self):
        return self.titulo


class AvisoTurma(models.Model):
    id = models.BigAutoField(primary_key=True)
    aviso = models.ForeignKey(
        Aviso,
        on_delete=models.CASCADE,
        db_column="aviso_id",
        related_name="avisos_turmas",
    )
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.CASCADE,
        db_column="turma_id",
        related_name="avisos_turmas",
    )

    class Meta:
        db_table = "avisos_turmas"
        constraints = [
            models.UniqueConstraint(fields=["aviso", "turma"], name="uq_aviso_turma"),
        ]

    def __str__(self):
        return f"{self.aviso.titulo} -> {self.turma.nome_turma}"

