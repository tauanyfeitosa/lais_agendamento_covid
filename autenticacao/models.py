from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from localflavor.br.models import BRCPFField

from autenticacao.manager import CandidatoManager
from base.models import BaseModel


class BaseUser(AbstractBaseUser, PermissionsMixin):
    cpf = BRCPFField(
        max_length=11,
        unique=True,
        verbose_name='CPF'
    )
    is_active = models.BooleanField(
        default=True
    )
    is_superuser = models.BooleanField(
        default=False
    )
    is_staff = models.BooleanField(
        default=False
    )
    USERNAME_FIELD = 'cpf'

    objects = CandidatoManager()

    def __str__(self):
        return self.cpf

    def clean(self):
        self.cpf = self.cpf.replace('.', '').replace('-', '')

    class Meta:
        verbose_name = u'Usuário Base'
        verbose_name_plural = u'Usuários Base'


class Candidato(BaseModel):
    candidato = models.OneToOneField(
        'BaseUser',
        on_delete=models.PROTECT,
        verbose_name=u'Usuário'
    )
    nome = models.CharField(
        max_length=255,
        verbose_name='Nome Completo'
    )
    data_nascimento = models.DateField(
        verbose_name='Data de Nascimento'
    )
    covid_30_dias = models.BooleanField(
        default=False,
        verbose_name='Teve COVID nos últimos 30 dias?'
    )

    @property
    def idade(self):
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year

        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1

        return idade

    @property
    def eh_apto_agendamento(self):
        if self.covid_30_dias:
            return False

        if self.idade < 18:
            return False

        nomes_grupos_nao_permitidos = [
            'População Privada de Liberdade',
            'Pessoas com Deficiência Institucionalizadas',
            'Pessoas ACAMADAS de 80 anos ou mais'
        ]

        grupos_nao_permitidos = self.grupos_atendimento.filter(
            grupo_atendimento__nome__in=nomes_grupos_nao_permitidos
        )

        if grupos_nao_permitidos.exists():
            return False

        return True

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'


class GrupoAtendimentoCandidato(BaseModel):
    candidato = models.ForeignKey(
        'Candidato',
        on_delete=models.PROTECT,
        verbose_name='Candidato',
        related_name='grupos_atendimento'
    )
    grupo_atendimento = models.ForeignKey(
        'base.GrupoAtendimento',
        on_delete=models.PROTECT,
        verbose_name='Grupo de Atendimento',
        related_name='candidatos'
    )

    def __str__(self):
        return f'{self.candidato} - {self.grupo_atendimento}'
