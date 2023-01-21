from utilities.models import models, CriadoAlteradoEm
from utilities.choices import FORMA_PAGAMENTO_CHOICES
from utilities.validators import numero_positivo


class Venda(CriadoAlteradoEm):
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES,
        default='AB'
    )
    finalizada = models.BooleanField(
        auto_created=True,
        default=False,
        verbose_name='Ativo'
    )

    def __str__(self):
        return f'{self.criado_em}'

    @property
    def qntd_produtos(self):
        ...

    @property
    def total(self):
        ...


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
