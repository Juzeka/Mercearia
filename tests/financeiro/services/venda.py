from django.test import TestCase
from apps.financeiro.models import Venda
from apps.financeiro.factories import (
    ItemVendaFactory,
    VendaFactory,
)
from apps.financeiro.services import VendaServices
from apps.produtos.factories import (
    CategoriaFactory,
    ProdutoFactory,
    ProdutoOrigemFactory
)
from parameterized import parameterized


HAS = [(True,),(False,)]


class VendaServicesTestCase(TestCase):
    class_model = Venda
    class_services = VendaServices

    @parameterized.expand(HAS)
    def test_has_origem(self, has):
        result = self.class_services(data={'produto_origem': has}).has_origem()

        self.assertEqual(result, has)

    def test_get_produto_origem(self):
        origem = ProdutoOrigemFactory(categoria=CategoriaFactory())

        result = self.class_services(
            data={'produto_origem': origem.pk}
        ).get_produto_origem().first()

        self.assertEqual(origem, result)

    @parameterized.expand(HAS)
    def test_nao_existe_produto_origem(self, has):
        data = {'produto_origem': False}

        if has:
            origem = ProdutoOrigemFactory(categoria=CategoriaFactory())
            data = {'produto_origem': origem.pk}

        result = self.class_services(data=data).nao_existe_produto_origem()

        self.assertEqual(has, result)

    def test_get_produto_false(self):
        data = {'produto_origem': False}

        result = self.class_services(data=data).get_produto()

        self.assertFalse(result)

    def test_verificar_quantidade(self):
        data_produto = {'categoria': CategoriaFactory(), 'quantidade':1}
        origem = ProdutoOrigemFactory(**data_produto)
        data_produto.update({'origem': origem})

        data = {'produto_origem': origem.pk, 'quantidade': 1}

        result = self.class_services(data=data).verificar_quantidade(
            ProdutoFactory(**data_produto)
        )

        self.assertEqual(0, result)

    @parameterized.expand([(4,6),(10,0)])
    def test_atualizar_estoque(self, qntd, expected):
        data_produto = {'categoria': CategoriaFactory(), 'quantidade': 10}
        origem = ProdutoOrigemFactory(**data_produto)
        data_produto.update({'origem': origem})

        data = {'produto_origem': origem.pk, 'quantidade': qntd}
        produto = ProdutoFactory(**data_produto)

        self.class_services(data=data).atualizar_estoque(produto)

        self.assertEqual(produto.quantidade, expected)
