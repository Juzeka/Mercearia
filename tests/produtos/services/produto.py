from django.test import TestCase
from apps.produtos.serializers import (
    ProdutoOrigemSerializer,
    ProdutoSerializer
)
from apps.produtos.factories import CategoriaFactory, ProdutoOrigemFactory
from apps.produtos.services import ProdutoServices
from apps.produtos.models import ProdutoOrigem
from parameterized import parameterized


DATA_AND_SERIALIZER = [
    (
        {
            'nome': 'Sonete Líquido',
            'descricao': 'líquido para lavar corpo.',
            'valor': 2.5,
            'quantidade': 200,
        },
        ProdutoOrigemSerializer
    ),
    (
        {
            'nome': 'Sonete Líquido',
            'descricao': 'líquido para lavar corpo.',
            'valor': 2.5,
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
