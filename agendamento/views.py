from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .excecoes import AgendamentoLotadoException
from .forms import AgendamentoForm
from .models import Agendamento


def get_horario_disponivel_por_idade(idade):
    if idade < 18:
        return None
    elif idade < 30:
        return '13h:00m'
    elif idade < 40:
        return '14h:00m'
    elif idade < 50:
        return '15h:00m'
    elif idade < 60:
        return '16h:00m'
    else:
        return '17h:00m'


def validar_idade_e_hora_agendamento(candidato, hora_agendamento):
    idade_candidato = candidato.idade
    if (idade_candidato < 18
            or (18 <= idade_candidato < 30 and hora_agendamento.hour != 13)
            or (30 <= idade_candidato < 40 and hora_agendamento.hour != 14)
            or (40 <= idade_candidato < 50 and hora_agendamento.hour != 15)
            or (50 <= idade_candidato < 60 and hora_agendamento.hour != 16)
            or (idade_candidato >= 60 and hora_agendamento.hour != 17)):
        return False
    return True


@login_required
def realizar_agendamento(request):
    candidato = request.user.candidato
    horario_disponivel = get_horario_disponivel_por_idade(candidato.idade)

    if not candidato.apto_agendamento:
        messages.warning(request, 'Você não está apto para realizar agendamentos.')
        return redirect('home')

    if candidato.get_agendamento():
        messages.error(request, 'Só é permitido um agendamento ativo por candidato.')
        return redirect('base:home')

    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.candidato = candidato

            if not validar_idade_e_hora_agendamento(candidato, agendamento.data_hora_agendamento):
                form.add_error('data_hora_agendamento', 'Horário do agendamento não corresponde à faixa etária do candidato.')
                return render(request, 'agendamento/realizar_agendamento.html', {'form': form})

            try:
                agendamento.save()
                messages.success(request, 'Agendamento realizado com sucesso.')
                return redirect('base:home')
            except AgendamentoLotadoException as e:
                form.add_error(e.field, e.args[0])

        return render(request, 'agendamento/realizar_agendamento.html', {'form': form, 'horario_disponivel': horario_disponivel})
    else:
        form = AgendamentoForm()
        return render(request, 'agendamento/realizar_agendamento.html', {'form': form, 'horario_disponivel': horario_disponivel})


@login_required
def vagas_disponiveis(request):
    limite_vagas = 5
    estabelecimento = request.GET.get('estabelecimento_saude_id')
    data_hora_agendamento = request.GET.get('data_hora_agendamento')

    agendamentos_realizados = Agendamento.objects.filter(
        estabelecimento_saude=estabelecimento,
        data_hora_agendamento__year=data_hora_agendamento.year,
        data_hora_agendamento__month=data_hora_agendamento.month,
        data_hora_agendamento__day=data_hora_agendamento.day,
        data_hora_agendamento__hour=data_hora_agendamento.hour
    ).count()

    vagas = limite_vagas - agendamentos_realizados
    return JsonResponse({'vagas': vagas})
