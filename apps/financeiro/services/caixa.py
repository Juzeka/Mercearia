from rest_framework.views import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


class CaixaServices:
    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.get('serializer')
        self.msg = kwargs.get('msg')

    def response_bad_request(self, condicao):
        if condicao:
            return Response({'msg': self.msg}, status=HTTP_400_BAD_REQUEST)

        return Response(self.serializer.data)
