from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from agendamento.excecoes import AgendamentoLotadoException
from base.models import BaseModel


class Agendamento(BaseModel):
    candidato = models.ForeignKey(
        'autenticacao.Candidato',
        on_delete=models.PROTECT,
        verbose_name='Candidato',
        related_name='agendamentos'
    )
    estabelecimento_saude = models.ForeignKey(
        'base.EstabelecimentoSaude',
        on_delete=models.PROTECT,
        verbose_name='Estabelecimento de Saúde',
        related_name='agendamentos'
    )
    data_hora_agendamento = models.DateTimeField(
        verbose_name='Data e Hora do Agendamento'
    )

    def atualizar_status_agendamento(self):
        if self.data_hora_agendamento < timezone.now():
            self.ativo = False
            self.save()
            return True
        return False

    def clean(self):
        if not self.ativo:
            return
        if self.data_hora_agendamento.weekday() not in [2,3,4,5]:
            raise ValidationError("Agendamentos só podem ser feitos de quarta-feira até sábado.")

        if self.data_hora_agendamento <= timezone.now():
            raise ValidationError("Agendamentos devem ser feitos para datas futuras.")

        if not 13 <= self.data_hora_agendamento.hour <= 17:
            raise ValidationError("Horário do agendamento deve ser entre 13h e 17h.")

    def save(self, *args, **kwargs):
        if self.ativo:
            if Agendamento.objects.filter(candidato=self.candidato, ativo=True).exists():
                raise ValidationError("O candidato já tem um agendamento ativo.")

            appointments_count = Agendamento.objects.filter(
                estabelecimento_saude=self.estabelecimento_saude,
                data_hora_agendamento__year=self.data_hora_agendamento.year,
                data_hora_agendamento__month=self.data_hora_agendamento.month,
                data_hora_agendamento__day=self.data_hora_agendamento.day,
                data_hora_agendamento__hour=self.data_hora_agendamento.hour
            ).count()
            if appointments_count >= 5:
                raise AgendamentoLotadoException("Não há mais vagas disponíveis neste horário para o estabelecimento selecionado.")

        self.full_clean()
        super(Agendamento, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.candidato.nome} - {self.data_hora_agendamento.strftime('%d/%m/%Y às %H:%M')} - {self.estabelecimento_saude}"

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
