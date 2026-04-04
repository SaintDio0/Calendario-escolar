from django.conf import settings
from django.db import models


class LogSistema(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        db_column="usuario_id",
        related_name="logs_sistema",
        null=True,
        blank=True,
    )
    acao = models.CharField(max_length=100)
    tabela_afetada = models.CharField(max_length=100, null=True, blank=True)
    registro_id = models.PositiveBigIntegerField(null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    ip_origem = models.CharField(max_length=45, null=True, blank=True)
    data_acao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "logs_sistema"
        ordering = ["-data_acao"]

    def __str__(self):
        return f"{self.acao} em {self.tabela_afetada or 'N/A'}"

