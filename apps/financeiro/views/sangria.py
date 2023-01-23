from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.decorators import action
from apps.financeiro.models import Sangria, Caixa
from apps.financeiro.serializers import SangriaSerializer, CaixaSerializer
from django.shortcuts import get_object_or_404
from decimal import Decimal


class SangriaViewSet(ModelViewSet):
    serializer_class = SangriaSerializer
    class_model = Sangria
    error = {'msg': 'Valor da sangria maior que o total em caixa.'}

    def get_queryset(self):
        return self.class_model.objects.all()

    @action(methods=['post'], detail=True, url_path='fazer_sangria')
    def fazer_sangria(self, request, *args, **kwargs):
        caixa = get_object_or_404(Caixa, pk=kwargs.get('pk'))

        sangria = Decimal(request.data.get('valor'))
        valor = caixa.total - sangria

        if valor >= 0:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)

            caixa_serializer = CaixaSerializer(caixa)
            caixa_serializer.instance.sangrias.add(serializer.instance)

            caixa_serializer = CaixaSerializer(caixa, data=caixa_serializer.data)
            caixa_serializer.is_valid(raise_exception=True)

            self.perform_update(caixa_serializer)

            return Response(serializer.data, HTTP_201_CREATED)

        return Response(self.error, HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path='editar_sangria')
    def editar(self, request, *args, **kwargs):
        sangria = Decimal(request.data.get('valor'))
        valor = get_object_or_404(Caixa, pk=kwargs.get('pk')).total - sangria

        if valor >= 0:
            return super().update(request, *args, **kwargs)

        return Response(self.error, HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        self.error = {'msg': 'Não é possível excluir uma sangria.'}

        return Response(self.error, HTTP_400_BAD_REQUEST)
