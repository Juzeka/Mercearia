from factory.django import DjangoModelFactory
from factory import Sequence
from ..models import Categoria


class CategoriaFactory(DjangoModelFactory):
    class Meta:
        model = Categoria
