from django.test import TestCase
from apps.produtos.serializers import (
    ProdutoOrigemSerializer,
    ProdutoSerializer
)
from apps.produtos.factories import CategoriaFactory, ProdutoOrigemFactory
from apps.produtos.services import ProdutoServices
from apps.produtos.models import ProdutoOrigem, Produto
from parameterized import parameterized
from rest_framework.utils.serializer_helpers import ReturnDict


DATA_AND_SERIALIZER = [
    (
        {
            'nome': 'Sonete Líquido',
            'descricao': 'líquido para lavar corpo.',
            'valor': 2.5,
            'quantidade': 400,
        },
        ProdutoOrigemSerializer
    ),
    (
        {
            'nome': 'Shampoo Líquido',
            'descricao': 'líquido para lavar cabelos.',
            'valor': 25.5,
            'quantidade': 200,
            'origem': True
        },
        ProdutoSerializer
    ),
]


class ProdutoServicesTestCase(TestCase):
    class_services = ProdutoServices

    def setUp(self):
        self.categoria = CategoriaFactory()

    @parameterized.expand(DATA_AND_SERIALIZER)
    def test_serializar_e_salvar(self, data, serializer):
        if data.get('origem'):
            data.pop('origem')
            data.update({'categoria': self.categoria})

            origem = ProdutoOrigemFactory(**data)

            data.update({'origem': origem.pk})

        data.update({'categoria': self.categoria.pk})

        response = self.class_services(
            data=data,
            serializer=serializer
        ).serialize_and_save()

        is_exists = ProdutoOrigem.objects.filter(
            pk=response.instance.pk
        ).exists()

        self.assertIsInstance(response, ProdutoOrigemSerializer)
        self.assertIsInstance(response.instance, ProdutoOrigem)
        self.assertTrue(is_exists)

    def test_criar_produto_com_origem(self):
        data = {
            'nome': 'Água sanitária',
            'descricao': 'líquido para lavar o chão.',
            'categoria': self.categoria.pk,
            'valor': 5.5,
            'quantidade': 500,
        }

        response = self.class_services(data=data).create_produto_com_origem()

        origem = ProdutoOrigem.objects.filter(**data).exists()
        produto = Produto.objects.filter(**data).exists()

        self.assertEqual(origem, produto)
        self.assertIsInstance(response, ReturnDict)
