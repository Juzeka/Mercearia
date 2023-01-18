from factory.django import DjangoModelFactory
from factory import Sequence
from ..models import Produto, ProdutoOrigem


class ProdutoOrigemFactory(DjangoModelFactory):
    class Meta:
        model = ProdutoOrigem

    nome = Sequence(lambda n: 'Produto %d' % n)


class ProdutoFactory(ProdutoOrigemFactory):
    class Meta:
        model = Produto
