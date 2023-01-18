from utilities.models import models, CriadoAlteradoEm


class ProdutoOrigem(CriadoAlteradoEm):
    nome = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Nome'
    )
    descricao = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    #categoria
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
