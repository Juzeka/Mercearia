from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from apps.financeiro.models import Venda
from apps.financeiro.factories import (
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
from apps.utilities.choices import FORMA_PAGAMENTO_CHOICES


EST_QNTD_PROD_STATUS =[
    (5, 4, True, HTTP_201_CREATED),
    (5, 6, True, HTTP_400_BAD_REQUEST),
    (5, 5, False, HTTP_404_NOT_FOUND),
]
QNTD_VENDAS_PG = [(5, 1), (10,2), (26, 3),]
QNTD_ITENS = [(5,), (10,), (26,),]
ITENS_STATUS = [
    (False, HTTP_204_NO_CONTENT),
    (True, HTTP_400_BAD_REQUEST),
]


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

    @parameterized.expand(EST_QNTD_PROD_STATUS)
    def test_criar_e_associar_item_de_venda(self, estoque, qntd, has_produto, status):
        condicao = estoque > qntd
        msg = 'Produto não existe no sistema.'

        venda = self.class_factory(**self.data)

        data = {
            'venda': venda.pk,
            'quantidade': qntd,
            'produto_origem': False
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
            self.assertEqual(response.status_code, status)
            self.assertEqual(data, expected)
        if (not condicao or not has_produto) or not condicao:
            self.assertEqual(response.data.get('msg'), msg)

    @parameterized.expand(QNTD_VENDAS_PG)
    def test_listar(self, qntd, forma_pagamento):
        self.class_factory.create_batch(
            size=qntd,
            finalizada= True,
            forma_pagamento = FORMA_PAGAMENTO_CHOICES[forma_pagamento][0]
        )

        response = self.client.get(self.class_router)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(qntd, len(response.data))

    @parameterized.expand(QNTD_ITENS)
    def test_listar_itens(self, qntd):
        produto = ProdutoFactory(valor=20.0, categoria=CategoriaFactory())
        venda = self.class_factory(**self.data)

        ItemVendaFactory.create_batch(
            size=qntd,
            venda=venda,
            produto=produto,
            quantidade=qntd
        )

        response = self.client.get(f'{self.class_router}{venda.pk}/itens_venda/')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(qntd, len(response.data))

    def test_detalhe(self):
        venda = self.class_factory(**{
            'finalizada': True,
            'forma_pagamento': FORMA_PAGAMENTO_CHOICES[1][0]
        })

        response = self.client.get(f'{self.class_router}{venda.pk}/')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIsInstance(response.data, ReturnDict)

    @parameterized.expand(ITENS_STATUS)
    def test_excluir(self, has_itens, status):
        venda = self.class_factory(**{
            'finalizada': True,
            'forma_pagamento': FORMA_PAGAMENTO_CHOICES[1][0]
        })

        if has_itens:
            ItemVendaFactory.create_batch(
                size=2,
                venda=venda,
                produto=ProdutoFactory(categoria=CategoriaFactory())
            )

        response = self.client.delete(
            f'{self.class_router}{venda.pk}/'
        )

        self.assertEqual(response.status_code, status)

    def test_excluir_item(self):
        item = ItemVendaFactory(
            venda=self.class_factory(**{
                'finalizada': True,
                'forma_pagamento': FORMA_PAGAMENTO_CHOICES[1][0]
            }),
            produto=ProdutoFactory(categoria=CategoriaFactory()),
            quantidade=3
        )

        response = self.client.delete(
            f'{self.class_router}{item.pk}/excluir_item/'
        )

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
