from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from apps.financeiro.models import Caixa
from apps.financeiro.factories import CaixaFactory
from apps.financeiro.services import CaixaServices
from apps.financeiro.serializers import CaixaSerializer
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
