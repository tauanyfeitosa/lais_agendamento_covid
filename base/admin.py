from django.contrib import admin
from .models import EstabelecimentoSaude

@admin.register(EstabelecimentoSaude)
class EstabelecimentoSaudeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo_cnes')
    search_fields = ('nome', 'codigo_cnes')

    class Meta:
        model = EstabelecimentoSaude
