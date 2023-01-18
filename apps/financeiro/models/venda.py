from utilities.models import models, CriadoAlteradoEm
from utilities.choices import FORMA_PAGAMENTO_CHOICES


class Venda(CriadoAlteradoEm):
    caixa = models.ForeignKey(
        'financeiro.Caixa',
        on_delete=models.PROTECT,
        verbose_name='Caixa'
    )
    produtos = models.ManyToManyField(
        'produtos.Produto',
        related_name='venda_produtos',
        verbose_name='Produtos da venda'
    )
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES,
        default='DI'
    )

    def __str__(self):
        return f'{self.criado_em} - {self.caixa.criado_em}'

    @property
    def qntd_produtos(self):
        return self.venda_produtos.count()

    @property
    def total(self):
        ...
