from rest_framework.views import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.shortcuts import render
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from weasyprint import HTML
from apps.financeiro.models import Caixa
from apps.produtos.models import ProdutoOrigem, Produto


class CaixaServices:
    class_model = Caixa
    template_name = 'financeiro/relatorio.html'

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.get('serializer')
        self.msg = kwargs.get('msg')
        self.request = kwargs.get('request')
        self.data = kwargs.get('data')
        self.pk = kwargs.get('pk')

    def response_bad_request(self, condicao):
        if condicao:
            return Response({'msg': self.msg}, status=HTTP_400_BAD_REQUEST)

        return Response(self.serializer.data)

    def get_data_relatorio(self):
        produtos = Produto.objects.all().values('pk')
        pks_excludes = [i.get('pk') for i in produtos]

        return {
            'caixa': get_object_or_404(
                self.class_model,
                pk=self.pk,
                aberto=False
            ),
            'produtos': ProdutoOrigem.objects.all().exclude(pk__in=pks_excludes)
        }

    def gerar_relatorio(self):
        return render(self.request, self.template_name, self.data)

    def relatorio_fechamento_pdf(self):
        template = get_template(self.template_name).render(self.data).encode(
            encoding='UTF-8'
        )

        return HTML(string=template).write_pdf()

