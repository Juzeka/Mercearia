from factory.django import DjangoModelFactory
from ..models import Venda, ItemVenda


class VendaFactory(DjangoModelFactory):
    class Meta:
        model = Venda


class ItemVendaFactory(DjangoModelFactory):
    class Meta:
        model = ItemVenda
