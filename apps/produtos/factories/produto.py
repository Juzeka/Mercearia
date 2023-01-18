from factory.django import DjangoModelFactory
from factory import Sequence
from ..models import Produto, ProdutoOrigem


class ProdutoOrigemFactory(DjangoModelFactory):
    class Meta:
        model = ProdutoOrigem


class ProdutoFactory(DjangoModelFactory):
    class Meta:
        model = Produto
