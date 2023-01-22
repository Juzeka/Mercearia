from utilities.models import models, CriadoAlteradoEm
from utilities.choices import FORMA_PAGAMENTO_CHOICES
from utilities.validators import numero_positivo
from django.db.models import Sum, F
from decimal import Decimal


class Venda(CriadoAlteradoEm):
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES,
        default='AB'
    )
    finalizada = models.BooleanField(
        auto_created=True,
        default=False,
        verbose_name='Finalizada'
    )

    def __str__(self):
        return f'{self.criado_em}'

    @property
    def qntd_itens(self):
        return self.item_venda_venda.all().count()

    @property
    def total(self):
        total = self.item_venda_venda.annotate(
            total_venda=models.ExpressionWrapper(
                F('produto__valor') * F('quantidade'),
                output_field=models.DecimalField()
            )
        )

        return Decimal(total.aggregate(total=Sum('total_venda'))['total'])


class ItemVenda(CriadoAlteradoEm):
    venda = models.ForeignKey(
        Venda,
        on_delete=models.PROTECT,
        related_name='item_venda_venda',
        verbose_name='Venda'
    )
    produto = models.ForeignKey(
        'produtos.Produto',
        on_delete=models.PROTECT,
        related_name='item_venda_produto',
        verbose_name='Produto da venda'
    )
    quantidade = models.IntegerField(
        blank=False,
        null=False,
        default=0,
        validators=[numero_positivo],
        verbose_name='Quantidade'
    )

    def __str__(self):
        return f'{self.venda} - {self.produto} - {self.quantidade}'

    @property
    def total(self):
        return self.quantidade * self.produto.valor
