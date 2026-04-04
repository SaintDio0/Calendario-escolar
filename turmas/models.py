from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class AnoLetivo(models.Model):
    id = models.BigAutoField(primary_key=True)
    ano = models.PositiveSmallIntegerField(
        unique=True,
        validators=[MinValueValidator(1901), MaxValueValidator(2155)],
    )
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "anos_letivos"
        ordering = ["-ano"]

    def __str__(self):
        return str(self.ano)


class Turma(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome_turma = models.CharField(max_length=100)
    serie = models.CharField(max_length=50)
    segmento = models.CharField(max_length=50, null=True, blank=True)
    turno = models.CharField(max_length=30, null=True, blank=True)
    ano_letivo = models.ForeignKey(
        AnoLetivo,
        on_delete=models.RESTRICT,
        db_column="ano_letivo_id",
        related_name="turmas",
    )
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "turmas"
        ordering = ["ano_letivo__ano", "serie", "nome_turma"]

    def __str__(self):
        return f"{self.nome_turma} ({self.serie})"


class Aluno(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    data_nascimento = models.DateField(null=True, blank=True)
    matricula = models.CharField(max_length=50, unique=True)
    turma = models.ForeignKey(
        Turma,
        on_delete=models.RESTRICT,
        db_column="turma_id",
        related_name="alunos",
        db_index=False,
    )
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "alunos"
        indexes = [
            models.Index(fields=["turma"], name="idx_alunos_turma"),
        ]
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} - {self.matricula}"

