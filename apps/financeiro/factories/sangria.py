from factory.django import DjangoModelFactory
from factory import Sequence
from ..models import Sangria


class SangriaFactory(DjangoModelFactory):
    class Meta:
        model = Sangria
