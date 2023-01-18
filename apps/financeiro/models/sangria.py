from utilities.models import models, CriadoAlteradoEm


class Sangria(CriadoAlteradoEm):
    valor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Valor'
    )
    descricao = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
