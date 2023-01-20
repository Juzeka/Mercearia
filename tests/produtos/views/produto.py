from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)
from apps.produtos.models import ProdutoOrigem, Produto
from apps.produtos.factories import (
    CategoriaFactory,
    ProdutoFactory,
    ProdutoOrigemFactory
)
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
QNTD_PRODUTOS = [(1, 54),(10, 500),(100, 140),(500, 233),]

class ProdutoViewSetTestCase(TestCase):
    class_model = ProdutoOrigem
    class_factory = ProdutoOrigemFactory
    class_router = '/api/produtos/'

    def setUp(self):
        self.categoria = CategoriaFactory()
        self.data = {
            'nome': 'Detergente Líquido',
            'descricao': 'Detergente líquido para lavar louças mais pesadas.',
            'categoria': self.categoria.pk,
            'valor': 2.50,
            'quantidade': 200,
        }

    def test_criar_produto(self):
        response = self.client.post(self.class_router, self.data)

        expected = {
            'nome': response.data.get('nome'),
            'descricao': response.data.get('descricao'),
            'categoria': response.data.get('categoria'),
            'valor': response.data.get('valor'),
            'quantidade': response.data.get('quantidade'),
        }

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(self.data, expected)

    @parameterized.expand(DATA_IN_ERROR)
    def test_criar_produto_sem_campos_obrigatorios(self, data, data_error):
        data.update({'categoria': self.categoria.pk})

        response = self.client.post(self.class_router, data)
        msg = response.data.get(data_error.get('campo'))[0].capitalize()

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(data_error.get('msg'), msg)

    def test_editar_produto_origem_sem_alterar_valor_do_produto(self):
        data = self.data.copy()

        data_edit = data.copy()
        data_edit.update({'nome': 'Líquido', 'valor': 50.0})
        data.update({'categoria': self.categoria})

        origem = self.class_factory(**data)
        data.update({'origem': origem})

        produto = ProdutoFactory(**data)

        response = self.client.put(
            f'{self.class_router}{origem.pk}/',
            data=data_edit,
            content_type='application/json'
        )

        produto_edit = Produto.objects.filter(pk=produto.pk).first()
        origem_edit = ProdutoOrigem.objects.filter(pk=origem.pk).first()

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertNotEqual(produto.nome, produto_edit.nome)
        self.assertNotEqual(origem.nome, origem_edit.nome)
        self.assertEqual(produto.valor, produto_edit.valor)
        self.assertNotEqual(origem.valor, origem_edit.valor)

    def test_excluir_produto_origem_sem_afetar_produto_vinculado(self):
        data = {
            'nome': 'Biscoito Maria',
            'descricao': 'Biscoito de agua e sal',
            'categoria': self.categoria,
            'valor': 2.50,
            'quantidade': 200,
        }

        origem = ProdutoOrigemFactory(**data)
        data.update({'origem': origem})
        produto = ProdutoFactory(**data)

        response = self.client.delete(f'{self.class_router}{origem.pk}/')

        instance_origem = ProdutoOrigem.objects.filter(pk=origem.pk)
        instance_produto = Produto.objects.filter(pk=produto.pk)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertFalse(instance_origem.exists())
        self.assertTrue(instance_produto.exists())

    @parameterized.expand(QNTD_PRODUTOS)
    def test_listar_produtos(self, qntd_produtos, qntd):
        origens = ProdutoOrigemFactory.create_batch(
            size=qntd_produtos,
            categoria=self.categoria,
            quantidade=qntd
        )

        response = self.client.get(self.class_router)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(qntd_produtos,len(response.data))
