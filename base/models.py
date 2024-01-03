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
