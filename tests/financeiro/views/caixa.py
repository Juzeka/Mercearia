from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from apps.financeiro.models import Caixa
from apps.financeiro.factories import (
    CaixaFactory,
    VendaFactory,
    ItemVendaFactory
)
from apps.financeiro.services import CaixaServices
from apps.produtos.factories import ProdutoFactory, CategoriaFactory
from apps.produtos.models import ProdutoOrigem
from parameterized import parameterized
from rest_framework.utils.serializer_helpers import ReturnDict


QNTD_VALOR_ABERTO = [(5, 34.0, True), (10, 230.5, False)]
DATA_STATUS = [
    ({'valor_inicial': 200.0, 'aberto': True}, HTTP_201_CREATED,),
    ({'aberto': True}, HTTP_400_BAD_REQUEST,),
]
ABERTO_STATUS_ERROR = [
    (True, HTTP_200_OK, False),
    (False, HTTP_400_BAD_REQUEST, False),
    (None, HTTP_404_NOT_FOUND, True),
]
ABERTO_STATUS_INSTANCE = [
    (False, HTTP_200_OK, ReturnDict, False),
    (True, HTTP_400_BAD_REQUEST, dict, False),
    (None, HTTP_404_NOT_FOUND, None, True),
]
ABERTO_VENDA_STATUS = [
    (True, False, HTTP_204_NO_CONTENT, False),
    (False, False, HTTP_204_NO_CONTENT, False),
    (True, True, HTTP_400_BAD_REQUEST, False),
    (False, True, HTTP_400_BAD_REQUEST, False),
    (None, None, HTTP_404_NOT_FOUND, True),
]
CONTENT_TYPE_URL = [
    ('application/pdf', '/relatorio_fechamento/pdf/',),
    ('text/html; charset=utf-8', '/relatorio_fechamento/',),
]


class CaixaViewSetTestCase(TestCase):
    class_model = Caixa
    class_factory = CaixaFactory
    class_services = CaixaServices
    class_router = '/api/financeiro/caixas/'

    def setUp(self):
        self.data = {'size': 1, 'valor_inicial': 50.0}

    def criar_caixas(self, data):
        return self.class_factory.create_batch(**data)

    @parameterized.expand(DATA_STATUS)
    def test_abrir_caixa(self, data, status):
        response = self.client.post(self.class_router, data=data)
        caixa = self.class_model.objects.filter(pk=response.data.get('id'))

        self.assertEqual(response.status_code, status)

        if data.get('valor_inicial'):
            self.assertTrue(caixa.exists())
        else:
            msg = response.data.get('valor_inicial')[0].capitalize()

            self.assertEqual(msg, 'Este campo ?? obrigat??rio.')

    @parameterized.expand(QNTD_VALOR_ABERTO)
    def test_listar_caixas(self, qntd, valor, aberto):
        url = self.class_router

        if aberto:
            url = f'{self.class_router}caixas_abertos/'

        self.criar_caixas({
            'size': qntd,
            'valor_inicial': valor,
            'aberto': aberto
        })

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(qntd,len(response.data))

    @parameterized.expand(ABERTO_STATUS_ERROR)
    def test_ver_caixa_aberto(self, aberto, status, error):
        pk = 0

        if not error:
            data = self.data.copy()
            data.update({'aberto': aberto})

            caixa = self.criar_caixas(data)[0]
            pk = caixa.pk

        response = self.client.get(f'{self.class_router}{pk}/aberto/')

        if not aberto and not error:
            msg = 'N??o ?? poss??vel ver caixa fechado.'

            self.assertEqual(msg, response.data.get('msg'))
        elif error:
            msg = response.data.get('detail').capitalize()

            self.assertEqual('N??o encontrado.', msg)

        self.assertEqual(response.status_code, status)

    @parameterized.expand(ABERTO_STATUS_INSTANCE)
    def test_detalhe(self, aberto, status, is_instance, error):
        pk = 0

        if not error:
            data = self.data.copy()
            data.update({'aberto': aberto})

            caixa = self.criar_caixas(data)[0]
            pk = caixa.pk

        response = self.client.get(f'{self.class_router}{pk}/')

        if not error:
            self.assertIsInstance(response.data, is_instance)
        else:
            msg = response.data.get('detail').capitalize()

            self.assertEqual('N??o encontrado.', msg)

        self.assertEqual(response.status_code, status)

    @parameterized.expand(ABERTO_VENDA_STATUS)
    def test_excluir_caixa(self, aberto, has_vendas, status, error):
        pk = 0

        if not error:
            data = self.data.copy()
            data.update({'aberto': aberto})

            caixa = self.criar_caixas(data)[0]

            if has_vendas:
                produto = ProdutoFactory(
                    categoria=CategoriaFactory(),
                    valor=23.5,
                    origem=None,
                    quantidade=3
                )
                venda = VendaFactory(forma_pagamento='AB')

                ItemVendaFactory(venda=venda, produto=produto, quantidade=2)

                caixa.vendas.add(venda)
                caixa.save()

            pk = caixa.pk

        response = self.client.delete(f'{self.class_router}{pk}/')

        self.assertEqual(response.status_code, status)

        if has_vendas:
            msg = 'N??o ?? poss??vel excluir caixa com vendas realizadas.'

            self.assertEqual(msg, response.data.get('msg'))
        elif error:
            msg = response.data.get('detail').capitalize()

            self.assertEqual('N??o encontrado.', msg)

    def test_fechamento_caixa(self):
        data = self.data.copy()
        data.update({'aberto': True})

        caixa = self.criar_caixas(data)[0]

        content_type = 'text/html; charset=utf-8'
        template = self.class_services(
            data={'caixa': caixa, 'produtos':ProdutoOrigem.objects.all()}
        ).gerar_relatorio()

        response = self.client.patch(f'{self.class_router}{caixa.pk}/fechar/')

        caixa_fechado = self.class_model.objects.get(pk=caixa.pk)

        self.assertEqual(response.status_code, template.status_code)
        self.assertEqual(response.content, template.content)
        self.assertEqual(response.headers.get('Content-type'), content_type)
        self.assertNotEqual(caixa.aberto, caixa_fechado.aberto)

    @parameterized.expand(CONTENT_TYPE_URL)
    def test_gerar_relatorio_fechamento(self, content_type, url):
        data = self.data.copy()
        data.update({'aberto': False})

        caixa = self.criar_caixas(data)[0]

        response = self.client.get(f'{self.class_router}{caixa.pk}{url}')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.headers.get('Content-type'), content_type)
