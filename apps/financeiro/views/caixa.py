from rest_framework.viewsets import ModelViewSet
from apps.financeiro.models import Caixa
from apps.financeiro.serializers import CaixaSerializer


class CaixaViewSet(ModelViewSet):
    serializer_class = CaixaSerializer
    class_model = Caixa
