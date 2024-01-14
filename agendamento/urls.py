from django.urls import path

from agendamento.views import realizar_agendamento, vagas_disponiveis

app_name = 'agendamento'

urlpatterns = [
    path('', realizar_agendamento, name='realizar_agendamento'),
    path('vagas_disponiveis/', vagas_disponiveis, name='vagas_disponiveis')
]