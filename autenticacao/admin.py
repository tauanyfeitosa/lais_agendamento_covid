from django.contrib import admin

from autenticacao.models import UsuarioBase, Candidato

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ('usuario_base', 'nome', 'apto_agendamento')
    search_fields = ('nome', 'apto_agendamento')
    list_filter = ('nome', 'apto_agendamento')
    change_list_template = 'admin/candidato/change_list.html'

    class Meta:
        model = Candidato


admin.site.register(UsuarioBase)
