from factory.django import DjangoModelFactory
from ..models import Venda


class VendaFactory(DjangoModelFactory):
    class Meta:
        model = Venda
