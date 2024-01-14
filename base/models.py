from django.db import models


class BaseModel(models.Model):
    """
    Modelo base com campos de data de criação, atualização e campo de ativo.
    """
    criado_em = models.DateTimeField(auto_now_add=True, editable=False)
    atualizado_em = models.DateTimeField(auto_now=True, editable=False)
    ativo = models.BooleanField(default=True, editable=False)

    class Meta:
        abstract = True


class GrupoAtendimento(models.Model):
    nome = models.CharField(max_length=255)
    codigo_si_pni = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Grupo de Atendimento'
        verbose_name_plural = 'Grupos de Atendimento'

    def __str__(self):
        return self.nome


class EstabelecimentoSaude(models.Model):
    nome = models.CharField(max_length=255)
    codigo_cnes = models.CharField(max_length=7)

    class Meta:
        verbose_name = u'Estabelecimento de Saúde'
        verbose_name_plural = u'Estabelecimentos de Saúde'

    def __str__(self):
        return f"{self.nome} - {self.codigo_cnes}"
