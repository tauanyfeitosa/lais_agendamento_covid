from django import forms

from agendamento.models import Agendamento


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['estabelecimento_saude', 'data_hora_agendamento']
        widgets = {
            'data_hora_agendamento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
