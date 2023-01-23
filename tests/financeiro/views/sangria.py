from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
from apps.financeiro.models import Sangria
from apps.financeiro.factories import (
    CaixaFactory,
    SangriaFactory,
)
from parameterized import parameterized
from rest_framework.utils.serializer_helpers import ReturnDict
from decimal import Decimal


QNTD_SANGRIAS = [(5,12.0), (10, 0.5),]
DATAS_STATUS_ERRO = [
    (
        {'valor': 20.4, 'descricao': 'Pagamento de agua'},
        HTTP_201_CREATED, False,
    ),
    (
        {'valor': 12.35, 'descricao': 'Reparo na pia'},
        HTTP_201_CREATED, False,
    ),
    (
        {'valor': 80.5, 'descricao': 'Reparo na pia'},
        HTTP_400_BAD_REQUEST, True,
    ),
    (
        {'valor': 90.0, 'descricao': 'Reparo na pia'},
        HTTP_400_BAD_REQUEST, True,
    ),
]
DATAS = [
    ({'valor': 20.4, 'descricao': 'Pagamento de agua'},),
    ({'valor': 12.35, 'descricao': 'Reparo na pia'},),
]


class SangriaViewSetTestCase(TestCase):
    class_model = Sangria
    class_factory = SangriaFactory
    class_router = '/api/financeiro/sangrias/'

    def setUp(self):
        self.sangria = self.class_factory(valor=20.25)

    @parameterized.expand(DATAS_STATUS_ERRO)
    def test_fazer_sangria(self, data, status, has_error):
        caixa = CaixaFactory(valor_inicial=100, aberto=True)
        caixa.sangrias.add(self.sangria)
        caixa.save()

        response = self.client.post(
            f'{self.class_router}{caixa.pk}/fazer_sangria/',
            data=data
        )

        if not has_error:
            sangria = self.class_model.objects.filter(pk=response.data.get('id'))
            self.assertTrue(sangria.exists())
        else:
            msg = 'Valor da sangria maior que o total em caixa.'

            self.assertEqual(response.data.get('msg'), msg)

        self.assertEqual(response.status_code, status)

    @parameterized.expand(QNTD_SANGRIAS)
    def test_listar(self, qntd, valor):
        self.class_factory.create_batch(qntd, valor=valor)

        response = self.client.get(self.class_router)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(qntd + 1, len(response.data))

    def test_detalhe(self):
        response = self.client.get(f'{self.class_router}{self.sangria.pk}/')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIsInstance(response.data, ReturnDict)

    @parameterized.expand(DATAS)
    def test_editar(self, data):
        caixa = CaixaFactory(valor_inicial=100, aberto=True)
        caixa.sangrias.add(self.sangria)
        caixa.save()

        data.update({
            'valor': Decimal(data.get('valor')).quantize(Decimal('.01'))
        })

        response = self.client.put(
            f'{self.class_router}{caixa.pk}/editar_sangria/',
            data=data,
            content_type='application/json'
        )

        result = {
            'valor':response.data.get('valor'),
            'descricao':response.data.get('descricao')
        }

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(data, result)

    def test_excluir(self):
        response = self.client.delete(
            f'{self.class_router}{self.sangria.pk}/'
        )
        instance = self.class_model.objects.filter(pk=self.sangria.pk)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertTrue(instance.exists())
