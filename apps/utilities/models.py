from django.db import models


class CriadoAlteradoEm(models.Model):
    class Meta:
        abstract = True

    criado_em = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name='Criado em'
    )
    alterado_em = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Alterado em'
    )
