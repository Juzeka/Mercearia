from django.test import TestCase
from apps.produtos.serializers import (
    ProdutoOrigemSerializer,
    ProdutoSerializer
)
from apps.produtos.factories import (
    CategoriaFactory,
    ProdutoOrigemFactory,
    ProdutoFactory
)
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
        self.data = {
            'nome': 'Água sanitária',
            'descricao': 'líquido para lavar o chão.',
            'categoria': self.categoria.pk,
            'valor': 5.5,
            'quantidade': 500,
        }

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
        response = self.class_services(data=self.data).create_produto_com_origem()

        origem = ProdutoOrigem.objects.filter(**self.data).exists()
        produto = Produto.objects.filter(**self.data).exists()

        self.assertEqual(origem, produto)
        self.assertIsInstance(response, ReturnDict)

    def test_editar_parcialmente_o_produto_e_produto_origem(self):
        data = self.data.copy()

        data_edit = data.copy()
        data_edit.update({'nome':'liquido', 'valor': 30.5})

        data.update({'categoria':self.categoria})
        origem = ProdutoOrigemFactory(**data)
        produto_origem = ProdutoOrigem.objects.get(pk=origem.pk)

        data.update({'categoria':self.categoria.pk})

        serializer = ProdutoOrigemSerializer(origem, data=data_edit)
        serializer.is_valid(raise_exception=True)

        data.update({'categoria': self.categoria, 'origem': origem})
        produto = ProdutoFactory(**data)
        data.update({'categoria': self.categoria.pk, 'origem': origem.pk})

        instances = self.class_services(
            data=data_edit,
            serializer=serializer,
            origem=origem.pk
        ).update_partial_in_produto()

        produto_edit = instances.get('produto', False)

        self.assertTrue(instances.get('origem', False))
        self.assertTrue(produto_edit)
        self.assertNotEqual(produto_origem.nome, origem.nome)
        self.assertNotEqual(produto_origem.valor, origem.valor)
        self.assertNotEqual(produto_edit.nome, produto.nome)
        self.assertEqual(produto_edit.valor, produto.valor)

    def test_editar_parcialmente_o_produto_origem_quando_nao_tem_produto(self):
        data = self.data.copy()

        data_edit = data.copy()
        data_edit.update({'nome':'liquido', 'valor': 30.5})

        data.update({'categoria':self.categoria})

        origem = ProdutoOrigemFactory(**data)
        produto_origem = ProdutoOrigem.objects.get(pk=origem.pk)

        data.update({'categoria':self.categoria.pk})

        serializer = ProdutoOrigemSerializer(origem, data=data_edit)
        serializer.is_valid(raise_exception=True)

        instances = self.class_services(
            data=data_edit,
            serializer=serializer,
            origem=origem.pk
        ).update_partial_in_produto()

        self.assertTrue(instances.get('origem', False))
        self.assertFalse(instances.get('produto', False))
        self.assertNotEqual(produto_origem.nome, origem.nome)
        self.assertNotEqual(produto_origem.valor, origem.valor)
