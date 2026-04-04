# Calendario Escolar Online (Django + MySQL)

Sistema web para calendario escolar com dois perfis principais:
- Responsavel: visualiza eventos e avisos permitidos.
- Gestor escolar (ADMIN, DIRETOR, PROFESSOR): gerencia eventos e avisos.

## Estrutura do projeto

```
calendario-main/
  calendario_escolar/
    settings.py
    urls.py
    config.py
  core/
    models.py (logs)
    views.py (dashboards e roteamento inicial)
    permissions.py
    management/commands/seed_data.py
  usuarios/
    models.py (Usuario custom + ResponsavelAluno)
    forms.py
    views.py (login/logout)
    admin.py
  turmas/
    models.py (AnoLetivo, Turma, Aluno)
    forms.py
    views.py
  eventos/
    models.py (TipoEvento, Evento, EventoTurma)
    forms.py
    services.py
    views.py (CRUD + calendario + API JSON)
  avisos/
    models.py (Aviso, AvisoTurma)
    forms.py
    services.py
    views.py (CRUD)
  templates/
    base.html
    registration/login.html
    core/*
    eventos/*
    avisos/*
    turmas/*
  static/
    css/main.css
    js/main.js
    js/calendar.js
```

## Tecnologias
- Python
- Django (ORM nativo)
- MySQL (XAMPP)
- HTML, CSS, Bootstrap 5
- JavaScript + FullCalendar

## Configuracao de banco
Arquivo principal: `calendario_escolar/config.py`

Padrao:
- engine: `django.db.backends.mysql`
- database: `calendario_escolar`
- host: `localhost`
- port: `3306`
- user: `root`
- password: vazio

## Comandos para executar localmente

1. Criar e ativar ambiente virtual (se ainda nao tiver):
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. (Opcional) Comandos base de criacao de projeto/apps em Django:
```bash
django-admin startproject calendario_escolar .
python manage.py startapp core
python manage.py startapp usuarios
python manage.py startapp turmas
python manage.py startapp eventos
python manage.py startapp avisos
```

4. Criar banco no MySQL (XAMPP):
```sql
CREATE DATABASE IF NOT EXISTS calendario_escolar
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

5. Gerar migrações (quando houver mudanca nos models):
```bash
python manage.py makemigrations
```

6. Aplicar migrações:
```bash
python manage.py migrate
```

7. Criar superusuario:
```bash
python manage.py createsuperuser
```

8. Popular com dados de exemplo:
```bash
python manage.py seed_data
```
Observação: esse comando limpa as tabelas de domínio e reinsere os dados padrão.

9. Subir servidor:
```bash
python manage.py runserver
```

## Login de demonstracao (apos `seed_data`)
- Admin: `admin@escola.com` / `123456`
- Diretor: `diretor@escola.com` / `123456`
- Professor: `professor@escola.com` / `123456`
- Responsável: `maria@escola.com` / `123456`

## Funcionalidades implementadas
- Login/logout com autenticacao Django
- Permissoes por perfil de usuario
- Dashboard do responsavel
- Dashboard do gestor
- CRUD completo de eventos
- Calendario visual mensal (FullCalendar)
- Filtros por tipo, turma e mes
- Tela de detalhes de evento
- CRUD de avisos
- Listagem de turmas
- Listagem de alunos
- Vinculacao de responsavel com aluno
- Mensagens amigaveis de sucesso/erro
- Paginacao nas listagens
