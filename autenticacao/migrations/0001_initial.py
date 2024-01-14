# Generated by Django 4.2.6 on 2024-01-13 05:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.br.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('cpf', localflavor.br.models.BRCPFField(max_length=14, unique=True, verbose_name='CPF')),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário Base',
                'verbose_name_plural': 'Usuários Base',
            },
        ),
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('ativo', models.BooleanField(default=True, editable=False)),
                ('nome', models.CharField(max_length=255, verbose_name='Nome Completo')),
                ('data_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('covid_30_dias', models.BooleanField(default=False, verbose_name='Teve COVID nos últimos 30 dias?')),
                ('apto_agendamento', models.BooleanField(default=False, verbose_name='É apto para agendamento?')),
                ('usuario_base', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Candidato',
                'verbose_name_plural': 'Candidatos',
            },
        ),
        migrations.CreateModel(
            name='GrupoAtendimentoCandidato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('ativo', models.BooleanField(default=True, editable=False)),
                ('candidato', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='grupos_atendimento', to='autenticacao.candidato', verbose_name='Candidato')),
                ('grupo_atendimento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='candidatos', to='base.grupoatendimento', verbose_name='Grupo de Atendimento')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
