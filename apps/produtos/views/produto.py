from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from ..serializers import ProdutoSerializer, ProdutoOrigemSerializer
from ..models import ProdutoOrigem
from ..services import ProdutoServices


class ProdutoViewSet(ModelViewSet):
    serializer_class = ProdutoOrigemSerializer
    class_model = ProdutoOrigem
    class_services = ProdutoServices

    def get_queryset(self):
        return self.class_model.objects.filter(ativo=True)

    def create(self, request, *args, **kwargs):
        origem = self.class_services(
            data=request.data
        ).create_produto_com_origem()

        headers = self.get_success_headers(origem)

        return Response(origem, status=HTTP_201_CREATED, headers=headers)
