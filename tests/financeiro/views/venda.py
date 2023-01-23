from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from apps.financeiro.models import Venda
from apps.financeiro.factories import (
    CaixaFactory,
    ItemVendaFactory,
    VendaFactory,
)
from apps.produtos.factories import (
    CategoriaFactory,
    ProdutoFactory,
    ProdutoOrigemFactory
)
from parameterized import parameterized
from rest_framework.utils.serializer_helpers import ReturnDict
from decimal import Decimal
from apps.utilities.choices import FORMA_PAGAMENTO_CHOICES


class VendaViewSetTestCase(TestCase):
    class_model = Venda
    class_factory = VendaFactory
    class_router = '/api/financeiro/vendas/'

    def setUp(self):
        self.data = {
            'finalizada': False,
            'forma_pagamento': FORMA_PAGAMENTO_CHOICES[0][0]
        }

    def test_abrir_venda(self):
        response = self.client.post(self.class_router, data=self.data)

        expected = {
            'finalizada': response.data.get('finalizada'),
            'forma_pagamento': response.data.get('forma_pagamento'),
        }

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(expected, self.data)

    @parameterized.expand([
        (5, 4, True, HTTP_201_CREATED),
        (5, 6, True, HTTP_400_BAD_REQUEST),
        (5, 4, False, HTTP_404_NOT_FOUND),
    ])
    def test_criar_e_associar_item_de_venda(self, estoque, qntd, has_produto, status):
        condicao = estoque > qntd
        msg = 'Produto não existe no sistema.'

        venda = VendaFactory(**self.data)

        data = {
            'venda': venda.pk,
            'quantidade': qntd,
            'produto_origem': None
        }

        if has_produto:
            msg = 'Quantidade insufíciente no estoque.'
            data_produto = {
                'valor': 20.0,
                'categoria': CategoriaFactory(),
                'quantidade': estoque
            }

            origem = ProdutoOrigemFactory(**data_produto)
            data_produto.update({'origem':origem})

            produto = ProdutoFactory(**data_produto)

            data.update({'produto_origem': origem.pk, 'produto': produto.pk})

        response = self.client.put(
            f'{self.class_router}{venda.pk}/criar_item_venda/',
            data=data,
            content_type='application/json'
        )

        data.pop('produto_origem')

        expected = {
            'venda': response.data.get('venda'),
            'quantidade': response.data.get('quantidade'),
            'produto': response.data.get('produto')
        }

        if condicao and has_produto:
            self.assertEqual(data, expected)
        if not condicao or not has_produto:
            self.assertEqual(response.data.get('msg'), msg)

        self.assertEqual(response.status_code, status)
