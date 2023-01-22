from utilities.models import models, CriadoAlteradoEm
from django.db.models import Sum, F
from decimal import Decimal


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
        return self.vendas.all().count()

    @property
    def total(self):
        total = self.valor_inicial
        vendas = self.vendas.annotate(
            total_venda=models.ExpressionWrapper(
                F('item_venda_venda__produto__valor') * F('item_venda_venda__quantidade'),
                output_field=models.DecimalField()
            )
        )

        total_vendas = vendas.aggregate(total=Sum('total_venda'))['total']
        total_sangrias = self.total_sangrias

        if total_vendas:
            total = total + total_vendas
        if total_sangrias:
            total = total - total_sangrias

        return Decimal(total)

    @property
    def qntd_sangrias(self):
        return self.sangrias.all().count()

    @property
    def qntd_itens_vendidos(self):
        return self.vendas.aggregate(
            qntd=Sum('item_venda_venda__quantidade')
        )['qntd']

    @property
    def total_sangrias(self):
        return self.sangrias.aggregate(total=Sum('valor'))['total']
