from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from rest_framework.decorators import action
from apps.financeiro.models import Venda, ItemVenda
from apps.financeiro.serializers import VendaSerializer, ItemVendaSerializer
from apps.financeiro.services import VendaServices
from apps.produtos.models import ProdutoOrigem, Produto
from apps.produtos.serializers import ProdutoOrigemSerializer
from django.shortcuts import get_object_or_404
from decimal import Decimal


class VendaViewSet(ModelViewSet):
    serializer_class = VendaSerializer
    class_model = Venda
    class_services = VendaServices

    def get_queryset(self):
        return self.class_model.objects.filter(finalizada=True)
    # listar o ProdutoOrigem quando criar o endpoint

    @action(methods=['put'], detail=True, url_path='criar_item_venda')
    def criar_item_para_venda(self, request, *args, **kwargs):
        error = {'msg': 'Produto não existe no sistema.'}
        data = request.data.copy()

        services = self.class_services(data=request.data.copy())

        if not services.nao_existe_produto_origem():
            return Response(error, status=HTTP_404_NOT_FOUND)

        produto = services.get_produto()
        has_quantidade = services.verificar_quantidade(produto)

        if has_quantidade >= 0:
            data.pop('produto_origem')

            item_venda = ItemVendaSerializer(data=data)
            item_venda.is_valid(raise_exception=True)

            self.perform_create(item_venda)

            services.atualizar_estoque(produto)

            headers = self.get_success_headers(item_venda.data)

            return Response(
                data=item_venda.data,
                status=HTTP_201_CREATED,
                headers=headers
            )

        return Response(
            data={'msg': 'Quantidade insufíciente no estoque.'},
            status=HTTP_400_BAD_REQUEST
        )
