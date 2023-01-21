from utilities.models import models, CriadoAlteradoEm


class Caixa(CriadoAlteradoEm):
    valor_inicial = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Valor'
    )
    vendas = models.ManyToManyField(
        'financeiro.Venda',
        blank=True,
        null=True,
        related_name='caixa_vendas',
        verbose_name='Vendas'
    )
    sangrias = models.ManyToManyField(
        'financeiro.Sangria',
        blank=True,
        null=True,
        related_name='caixa_sangrias',
        verbose_name='Sangrias'
    )
    aberto = models.BooleanField(
        auto_created=True,
        default=True,
        verbose_name='Aberto'
    )
    fechado_em = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Fechado em'
    )

    def __str__(self):
        return f'{self.criado_em}'

    @property
    def qntd_vendas(self):
        ...

    @property
    def total(self):
        ...
