from factory.django import DjangoModelFactory
from ..models import Caixa


class CaixaFactory(DjangoModelFactory):
    class Meta:
        model = Caixa
