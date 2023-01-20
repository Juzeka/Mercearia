from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)
from apps.produtos.models import Categoria
from apps.produtos.factories import (
    CategoriaFactory,
)
from parameterized import parameterized


QNTD_CATEGORIAS = [(5,), (10,), (100,),]
DATAS = [
    ({'nome': 'Frios', 'descricao': 'Setor de firos e congelados'},),
    ({'nome': 'Grãos', 'descricao': 'Setor de grãos'},),
]

class CategoriaViewSetTestCase(TestCase):
    class_model = Categoria
    class_factory = CategoriaFactory
    class_router = '/api/categorias/'

    def setUp(self):
        self.categoria = self.class_factory()

    @parameterized.expand(DATAS)
    def test_criar(self, data):
        response = self.client.post(self.class_router, data=data)

        categoria = self.class_model.objects.filter(pk=response.data.get('id'))

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertTrue(categoria.exists())

    @parameterized.expand(QNTD_CATEGORIAS)
    def test_listar(self, qntd):
        self.class_factory.create_batch(qntd)

        response = self.client.get(self.class_router)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(qntd, len(response.data))

    @parameterized.expand(DATAS)
    def test_editar(self, data):
        response = self.client.put(
            f'{self.class_router}{self.categoria.pk}/',
            data=data,
            content_type='application/json'
        )

        result = {
            'nome':response.data.get('nome'),
            'descricao':response.data.get('descricao')
        }

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(data, result)

    def test_excluir(self):
        instance = self.class_factory()

        response = self.client.delete(
            f'{self.class_router}{instance.pk}/'
        )
        categoria = self.class_model.objects.filter(pk=instance.pk)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertFalse(categoria.exists())
