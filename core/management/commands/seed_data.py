from datetime import date, datetime, time

from django.core.management.base import BaseCommand
from django.db import connection, transaction

from avisos.models import Aviso
from eventos.models import Evento, EventoTurma, TipoEvento
from turmas.models import Aluno, AnoLetivo, Turma
from usuarios.models import ResponsavelAluno, Usuario


class Command(BaseCommand):
    help = "Popula o banco com os dados padrão do projeto integrador."

    def _resetar_tabelas_dominio(self):
        tabelas = [
            "eventos_turmas",
            "avisos_turmas",
            "responsaveis_alunos",
            "eventos",
            "avisos",
            "alunos",
            "turmas",
            "anos_letivos",
            "tipos_evento",
            "logs_sistema",
            "usuarios",
        ]
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            for tabela in tabelas:
                cursor.execute(f"TRUNCATE TABLE {tabela};")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    @transaction.atomic
    def handle(self, *args, **options):
        self._resetar_tabelas_dominio()

        ano_letivo, _ = AnoLetivo.objects.update_or_create(
            ano=2026,
            defaults={"ativo": True},
        )

        turma_1, _ = Turma.objects.update_or_create(
            nome_turma="1º Ano A",
            ano_letivo=ano_letivo,
            defaults={
                "serie": "1º Ano",
                "segmento": "Fundamental I",
                "turno": "Manhã",
                "ativo": True,
            },
        )
        turma_2, _ = Turma.objects.update_or_create(
            nome_turma="2º Ano A",
            ano_letivo=ano_letivo,
            defaults={
                "serie": "2º Ano",
                "segmento": "Fundamental I",
                "turno": "Manhã",
                "ativo": True,
            },
        )
        turma_3, _ = Turma.objects.update_or_create(
            nome_turma="3º Ano A",
            ano_letivo=ano_letivo,
            defaults={
                "serie": "3º Ano",
                "segmento": "Fundamental I",
                "turno": "Tarde",
                "ativo": True,
            },
        )

        tipos_payload = [
            ("Prova", "#0d6efd", "bi bi-journal-text"),
            ("Reunião", "#198754", "bi bi-people"),
            ("Feriado", "#dc3545", "bi bi-calendar-x"),
            ("Evento Escolar", "#ffc107", "bi bi-calendar-event"),
            ("Entrega de Boletim", "#6f42c1", "bi bi-file-earmark-text"),
        ]
        tipos_evento = {}
        for nome, cor, icone in tipos_payload:
            tipo, _ = TipoEvento.objects.update_or_create(
                nome=nome,
                defaults={"cor": cor, "icone": icone, "ativo": True},
            )
            tipos_evento[nome] = tipo

        admin, _ = Usuario.objects.update_or_create(
            email="admin@escola.com",
            defaults={
                "nome": "Administrador do Sistema",
                "tipo_usuario": Usuario.TipoUsuario.ADMIN,
                "telefone": "(17)99999-0001",
                "ativo": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.set_password("123456")
        admin.save(update_fields=["password"])

        diretor, _ = Usuario.objects.update_or_create(
            email="diretor@escola.com",
            defaults={
                "nome": "Diretor Escolar",
                "tipo_usuario": Usuario.TipoUsuario.DIRETOR,
                "telefone": "(17)99999-0002",
                "ativo": True,
                "is_staff": True,
                "is_superuser": False,
            },
        )
        diretor.set_password("123456")
        diretor.save(update_fields=["password"])

        professor, _ = Usuario.objects.update_or_create(
            email="professor@escola.com",
            defaults={
                "nome": "Professor João",
                "tipo_usuario": Usuario.TipoUsuario.PROFESSOR,
                "telefone": "(17)99999-0003",
                "ativo": True,
                "is_staff": True,
                "is_superuser": False,
            },
        )
        professor.set_password("123456")
        professor.save(update_fields=["password"])

        responsavel, _ = Usuario.objects.update_or_create(
            email="maria@escola.com",
            defaults={
                "nome": "Maria Responsável",
                "tipo_usuario": Usuario.TipoUsuario.RESPONSAVEL,
                "telefone": "(17)99999-0004",
                "ativo": True,
                "is_staff": False,
                "is_superuser": False,
            },
        )
        responsavel.set_password("123456")
        responsavel.save(update_fields=["password"])

        aluno_1, _ = Aluno.objects.update_or_create(
            matricula="MAT2026001",
            defaults={
                "nome": "Pedro Henrique",
                "data_nascimento": date(2018, 5, 10),
                "turma": turma_1,
                "ativo": True,
            },
        )
        aluno_2, _ = Aluno.objects.update_or_create(
            matricula="MAT2026002",
            defaults={
                "nome": "Ana Julia",
                "data_nascimento": date(2017, 8, 22),
                "turma": turma_2,
                "ativo": True,
            },
        )

        ResponsavelAluno.objects.update_or_create(
            usuario=responsavel,
            aluno=aluno_1,
            defaults={"parentesco": "Mãe", "responsavel_principal": True},
        )
        ResponsavelAluno.objects.update_or_create(
            usuario=responsavel,
            aluno=aluno_2,
            defaults={"parentesco": "Mãe", "responsavel_principal": True},
        )

        reuniao_pais, _ = Evento.objects.update_or_create(
            titulo="Reunião de Pais",
            data_inicio=date(2026, 4, 10),
            defaults={
                "descricao": "Reunião geral para alinhamento do início do bimestre.",
                "data_fim": date(2026, 4, 10),
                "hora_inicio": time(19, 0, 0),
                "hora_fim": time(20, 30, 0),
                "tipo_evento": tipos_evento["Reunião"],
                "criado_por": diretor,
                "escopo": Evento.Escopo.GERAL,
                "prioridade": Evento.Prioridade.ALTA,
                "local_evento": "Auditório da escola",
                "publico": Evento.Publico.PAIS,
                "publicado": True,
                "ativo": True,
            },
        )

        prova_matematica, _ = Evento.objects.update_or_create(
            titulo="Prova de Matemática",
            data_inicio=date(2026, 4, 15),
            defaults={
                "descricao": "Avaliação bimestral de matemática do 1º Ano A.",
                "data_fim": date(2026, 4, 15),
                "hora_inicio": time(8, 0, 0),
                "hora_fim": time(9, 30, 0),
                "tipo_evento": tipos_evento["Prova"],
                "criado_por": professor,
                "escopo": Evento.Escopo.TURMA,
                "prioridade": Evento.Prioridade.NORMAL,
                "local_evento": "Sala 3",
                "publico": Evento.Publico.TODOS,
                "publicado": True,
                "ativo": True,
            },
        )

        feriado_tiradentes, _ = Evento.objects.update_or_create(
            titulo="Feriado de Tiradentes",
            data_inicio=date(2026, 4, 21),
            defaults={
                "descricao": "Feriado nacional.",
                "data_fim": date(2026, 4, 21),
                "hora_inicio": None,
                "hora_fim": None,
                "tipo_evento": tipos_evento["Feriado"],
                "criado_por": admin,
                "escopo": Evento.Escopo.GERAL,
                "prioridade": Evento.Prioridade.NORMAL,
                "local_evento": None,
                "publico": Evento.Publico.TODOS,
                "publicado": True,
                "ativo": True,
            },
        )

        EventoTurma.objects.update_or_create(evento=prova_matematica, turma=turma_1)
        EventoTurma.objects.filter(evento=prova_matematica).exclude(turma=turma_1).delete()
        EventoTurma.objects.filter(evento=reuniao_pais).delete()
        EventoTurma.objects.filter(evento=feriado_tiradentes).delete()

        Aviso.objects.update_or_create(
            titulo="Entrega de uniformes",
            defaults={
                "mensagem": "Os uniformes estarão disponíveis para retirada na secretaria até sexta-feira.",
                "publicado_por": diretor,
                "data_expiracao": datetime(2026, 4, 12, 18, 0, 0),
                "escopo": Aviso.Escopo.GERAL,
                "ativo": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Dados adaptados conforme inserts e aplicados com sucesso."))
        self.stdout.write("Logins: admin@escola.com / 123456, diretor@escola.com / 123456, professor@escola.com / 123456, maria@escola.com / 123456")
