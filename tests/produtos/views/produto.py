from django.test import TestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from apps.produtos.models import Produto
from apps.produtos.factories import ProdutoFactory, CategoriaFactory


class ProdutoViewSetTestCase(TestCase):
    class_model = Produto
    class_factory = ProdutoFactory
    class_router = '/api/produtos/'

    def setUp(self):
        self.categoria = CategoriaFactory()

    def test_criar_produto(self):
        data = {
            'nome': 'Detergente Líquido',
            'descricao': 'Detergente líquido para lavar louças mais pesadas.',
            'categoria': self.categoria.pk,
            'valor': 2.50,
            'quantidade': 200,
        }

        response = self.client.post(self.class_router, data)

        expected = {
            'nome': response.data.get('nome'),
            'descricao': response.data.get('descricao'),
            'categoria': response.data.get('categoria'),
            'valor': response.data.get('valor'),
            'quantidade': response.data.get('quantidade'),
        }

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(data, expected)
