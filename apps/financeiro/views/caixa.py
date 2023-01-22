from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.views import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT
)
from django.http.response import HttpResponse
from apps.financeiro.models import Caixa
from apps.financeiro.serializers import CaixaSerializer
from apps.financeiro.services import CaixaServices
from django.shortcuts import get_object_or_404


class CaixaViewSet(ModelViewSet):
    serializer_class = CaixaSerializer
    class_model = Caixa
    class_services = CaixaServices

    def get_queryset(self):
        return self.class_model.objects.filter(aberto=False)

    @action(methods=['get'], detail=False, url_path='caixas_abertos')
    def get_caixas_abertos(self, request, *args, **kwargs):
        caixas = self.class_model.objects.filter(aberto=True)
        serializer = self.get_serializer(caixas, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='aberto')
    def get_caixa_aberto(self, request, *args, **kwargs):
        caixa = get_object_or_404(self.class_model, pk=kwargs.get('pk'))
        serializer = self.serializer_class(caixa)

        return self.class_services(
            serializer=serializer,
            msg='Não é possível ver caixa fechado.'
        ).response_bad_request((not caixa.aberto))

    def retrieve(self, request, *args, **kwargs):
        caixa = get_object_or_404(self.class_model, pk=kwargs.get('pk'))
        serializer = self.serializer_class(caixa)

        return self.class_services(
            serializer=serializer,
            msg='Não é possível acessar detalhes do caixa com ele aberto.'
        ).response_bad_request(caixa.aberto)

    def destroy(self, request, *args, **kwargs):
        caixa = get_object_or_404(self.class_model, pk=kwargs.get('pk'))

        if caixa.vendas.all().exists():
            return Response(
                {'msg': 'Não é possível excluir caixa com vendas realizadas.'},
                status=HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(caixa)

        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['patch'], detail=True, url_path='fechar')
    def fechar_caixa(self, request, *args, **kwargs):
        caixa = get_object_or_404(self.class_model, pk=kwargs.get('pk'))

        serializer = self.get_serializer(
            caixa,
            data={'aberto': False},
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return self.class_services(
            request=request,
            data=self.class_services(pk=kwargs.get('pk')).get_data_relatorio()
        ).gerar_relatorio()

    @action(methods=['get'], detail=True, url_path='relatorio_fechamento')
    def get_relatorio_fechamento_html(self, request, *args, **kwargs):
        return self.class_services(
            request=request,
            data=self.class_services(pk=kwargs.get('pk')).get_data_relatorio()
        ).gerar_relatorio()

    @action(methods=['get'], detail=True, url_path='relatorio_fechamento/pdf')
    def get_relatorio_fechamento_pdf(self, request, *args, **kwargs):
        relatorio = self.class_services(
            data=self.class_services(pk=kwargs.get('pk')).get_data_relatorio()
        ).relatorio_fechamento_pdf()

        return HttpResponse(relatorio, content_type='application/pdf')
