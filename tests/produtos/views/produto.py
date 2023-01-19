from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
from apps.produtos.models import Produto
from apps.produtos.factories import ProdutoFactory, CategoriaFactory
from parameterized import parameterized


DATA_IN_ERROR = [
    (
        {
            'nome': 'Detergente Líquido',
            'descricao': 'líquido para lavar louças mais pesadas.',
            'valor': '',
            'quantidade': 200,
        },
        {
            'campo': 'valor',
            'msg': 'Um número válido é necessário.'
        }
    ),
    (
        {
            'nome': 'Amaciante Líquido',
            'descricao': 'líquido para perfurmar suas roupas.',
            'valor': 15.50,
            'quantidade': '20o',
        },
        {
            'campo': 'quantidade',
            'msg': 'Um número inteiro válido é exigido.'
        }
    ),
    (
        {
            'nome': 'Amaciante Líquido',
            'descricao': 'líquido para perfurmar suas roupas.',
            'valor': 15.50,
            'quantidade': -20,
        },
        {
            'campo': 'quantidade',
            'msg': 'Um número positivo é exigido.'
        }
    )
]


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

    @parameterized.expand(DATA_IN_ERROR)
    def test_criar_produto_sem_campos_obrigatorios(self, data, data_error):
        data.update({'categoria': self.categoria.pk})

        response = self.client.post(self.class_router, data)
        msg = response.data.get(data_error.get('campo'))[0].capitalize()

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(data_error.get('msg'), msg)
