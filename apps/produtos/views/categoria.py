from rest_framework.viewsets import ModelViewSet
from ..serializers import CategoriaSerializer
from ..models import Categoria


class CategoriaViewSet(ModelViewSet):
    serializer_class = CategoriaSerializer
    class_model = Categoria
