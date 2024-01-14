from django.urls import path

from base.views import home, grafico_aptos_inaptos, grafico_estabelecimento_agendamentos

app_name = 'base'

urlpatterns = [
    path('', home, name='home'),
    path('graficos/aptos_inaptos/', grafico_aptos_inaptos, name='grafico_aptos_inaptos'),
    path('graficos/agendamentos/', grafico_estabelecimento_agendamentos, name='grafico_agendamentos')
]
