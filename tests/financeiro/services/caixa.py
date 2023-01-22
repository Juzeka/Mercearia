from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from django.http.response import HttpResponse
from apps.financeiro.models import Caixa
from apps.financeiro.factories import CaixaFactory
from apps.financeiro.services import CaixaServices
from apps.financeiro.serializers import CaixaSerializer
from apps.produtos.factories import CategoriaFactory, ProdutoOrigemFactory
from apps.produtos.models import ProdutoOrigem
from parameterized import parameterized


ABERTO_MSG_STATUS = [
    (
        True,
        'Não é possível acessar detalhes do caixa com ele aberto.',
        False,
        HTTP_400_BAD_REQUEST,
    ),
    (False, None, False, HTTP_200_OK,),
    (False, 'Não é possível ver caixa fechado.', True, HTTP_400_BAD_REQUEST,),
    (True, None, True, HTTP_200_OK,),
]
HAS_PRODUTO = [(False,), (True,), (None,),]
CONTENT_TYPE_HTML = [
    ('application/pdf', False),
    ('text/html; charset=utf-8', True),
]


class CaixaServicesTestCase(TestCase):
    class_model = Caixa
    class_serializer = CaixaSerializer
    class_factory = CaixaFactory
    class_services = CaixaServices

    def setUp(self):
        self.data = {'valor_inicial': 31.28}

    @parameterized.expand(ABERTO_MSG_STATUS)
    def test_levantar_errors(self, aberto, msg, is_not, status):
        data = self.data.copy()
        data.update({'aberto': aberto})

        caixa = CaixaFactory(**data)
        serializer = CaixaSerializer(caixa)

        condicao = not caixa.aberto if is_not else caixa.aberto

        result = self.class_services(
            serializer=serializer,
            msg=msg
        ).response_bad_request(condicao)

        if msg is None:
            instance = self.class_model.objects.filter(pk=result.data.get('id'))
            self.assertTrue(instance.exists())
        else:
            self.assertEqual(msg, result.data.get('msg'))

        self.assertEqual(result.status_code, status)

    @parameterized.expand(HAS_PRODUTO)
    def test_pegar_dados_do_relatorio(self, has_produto):
        data = self.data.copy()
        data.update({'aberto': False})

        caixa = self.class_factory(**data)

        if has_produto:
            ProdutoOrigemFactory.create_batch(
                size=2,
                valor=14.0,
                categoria=CategoriaFactory()
            )

        result = self.class_services(pk=caixa.pk).get_data_relatorio()

        exists_produtos = self.assertTrue if has_produto else self.assertFalse

        exists_produtos(result.get('produtos').exists())
        self.assertIsInstance(result.get('caixa'), self.class_model)

    @parameterized.expand(CONTENT_TYPE_HTML)
    def test_gerar_relatorio(self, content_type, is_html):
        data = self.data.copy()
        data.update({'aberto': False})

        ProdutoOrigemFactory.create_batch(
            size=2,
            valor=14.0,
            categoria=CategoriaFactory()
        )

        caixa = CaixaFactory(**data)
        dados = {'caixa': caixa, 'produtos': ProdutoOrigem.objects.all()}

        services = self.class_services(data=dados)

        if is_html:
            result = services.gerar_relatorio()

            self.assertEqual(result.status_code, HTTP_200_OK)
            self.assertEqual(result.headers.get('Content-type'), content_type)
        else:
            result = services.relatorio_fechamento_pdf()
            response = HttpResponse(result, content_type)

            self.assertIsInstance(response, HttpResponse)
            self.assertEqual(response.status_code, HTTP_200_OK)
