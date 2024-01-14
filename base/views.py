from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect

from agendamento.models import Agendamento
from autenticacao.models import Candidato


@login_required
def home(request):
    usuario_base = request.user
    candidato = usuario_base.candidato
    if candidato.agendamentos.filter(ativo=True).exists():
        agendamento_ativo = candidato.agendamentos.filter(ativo=True).first().atualizar_status_agendamento()
    agendamentos = candidato.agendamentos.all()

    return render(request, 'home.html', locals())


@login_required
def grafico_aptos_inaptos(request):
    if not request.user.is_superuser or not request.user.is_staff:
        return redirect('base:home')

    queryset = Candidato.objects.all()
    qtd_aptos = queryset.filter(apto_agendamento=True).count()
    qtd_inaptos = queryset.filter(apto_agendamento=False).count()

    context = {
        'aptos': qtd_aptos,
        'inaptos': qtd_inaptos,
    }

    return render(request, 'graficos/aptos_inaptos.html', context)


@login_required
def grafico_estabelecimento_agendamentos(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('base:home')

    queryset = Agendamento.objects.values('estabelecimento_saude__nome').annotate(total=Count('id')).order_by('-total')

    nome_estabelecimentos = [item['estabelecimento_saude__nome'] for item in queryset]
    numero_agendamentos = [item['total'] for item in queryset]

    context = {
        'nome_estabelecimentos': nome_estabelecimentos,
        'numero_agendamentos': numero_agendamentos,
    }

    return render(request, 'graficos/agendamentos.html', context)
