# Generated by Django 4.2.6 on 2024-01-03 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('autenticacao', '0003_candidato_candidato'),
    ]

    operations = [
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
