from utilities.models import models, CriadoAlteradoEm, NomeDescricao
from utilities.validators import numero_positivo
from django.db.models import Sum, F


class ProdutoOrigem(CriadoAlteradoEm, NomeDescricao):
    categoria = models.ForeignKey(
        'produtos.Categoria',
        on_delete=models.PROTECT,
        verbose_name='Categoria'
    )
    valor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Valor'
    )
    quantidade = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        validators=[numero_positivo],
        verbose_name='Quantidade'
    )
    ativo = models.BooleanField(
        auto_created=True,
        default=True,
        verbose_name='Ativo'
    )

    @property
    def total_produto(self):
        return self.quantidade * self.valor


class Produto(ProdutoOrigem):
    origem = models.ForeignKey(
        ProdutoOrigem,
        on_delete=models.SET_NULL,
        null=True,
        related_name='produto_origem',
        verbose_name='Produto de origem',
    )
