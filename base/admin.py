from django.contrib import admin

from autenticacao.models import GrupoAtendimentoCandidato
from .models import EstabelecimentoSaude, GrupoAtendimento

from django.contrib.auth.models import Group


@admin.register(EstabelecimentoSaude)
class EstabelecimentoSaudeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo_cnes')
    search_fields = ('nome', 'codigo_cnes')
    list_filter = ('nome', 'codigo_cnes')
    change_list_template = 'admin/estabelecimento_saude/change_list.html'

    class Meta:
        model = EstabelecimentoSaude


admin.site.unregister(Group)

admin.site.register(GrupoAtendimento)
admin.site.register(GrupoAtendimentoCandidato)
