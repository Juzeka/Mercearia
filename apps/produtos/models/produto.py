from utilities.models import models, CriadoAlteradoEm, NomeDescricao


class ProdutoOrigem(CriadoAlteradoEm, NomeDescricao):
    categoria = models.ForeignKey(
        'produtos.Categoria',
        on_delete=models.PROTECT,
        verbose_name='Categoria'
    )
    valor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Valor'
    )
    quantidade = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='Quantidade'
    )
    ativo = models.BooleanField(
        auto_created=True,
        default=True,
        verbose_name='Ativo'
    )


class Produto(ProdutoOrigem):
    origem = models.ForeignKey(
        ProdutoOrigem,
        on_delete=models.PROTECT,
        verbose_name='Produto de origem',
    )
