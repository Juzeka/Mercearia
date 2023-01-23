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
from apps.utilities.choices import FORMA_PAGAMENTO_CHOICES


class VendaViewSet(ModelViewSet):
    serializer_class = VendaSerializer
    class_model = Venda
    class_services = VendaServices

    def get_queryset(self):
        return self.class_model.objects.filter(
            finalizada=True,
            forma_pagamento__in=[
                FORMA_PAGAMENTO_CHOICES[1][0],
                FORMA_PAGAMENTO_CHOICES[2][0],
                FORMA_PAGAMENTO_CHOICES[3][0]
            ]
        )

    @action(methods=['get'], detail=True, url_path='itens_venda')
    def get_listar_itens_venda(self, request, *args, **kwargs):
        queryset = ItemVenda.objects.filter(venda=kwargs.get('pk'))
        serializer = ItemVendaSerializer(queryset, many=True)

        return Response(serializer.data)

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.item_venda_venda.all().exists():
            return Response(
                {'msg': 'Impossível excluir venda com itens vinculados a ela.'},
                HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)
