from apps.produtos.serializers import (
    ProdutoSerializer,
    ProdutoOrigemSerializer
)
from apps.produtos.models import Produto


class ProdutoServices:
    def __init__(self, *args, **kwargs):
        self.data = kwargs.get('data')
        self.serializer = kwargs.get('serializer')
        self.origem = kwargs.get('origem')

    def serialize_and_save(self):
        serializer = self.serializer(data=self.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return serializer

    def create_produto_com_origem(self):
        self.serializer = ProdutoOrigemSerializer
        origem = self.serialize_and_save()

        data = self.data.copy()
        data.update({'origem': origem.instance.pk})
        self.data = data

        self.serializer = ProdutoSerializer
        self.serialize_and_save()

        return origem.data

    def update_partial_in_produto(self):
        instances = {}
        data = self.data.copy()
        data.pop('valor')

        instance = Produto.objects.filter(origem=self.origem)

        if instance.exists():
            instance = instance.first()

            produto = ProdutoSerializer(instance, data=data, partial=True)
            produto.is_valid(raise_exception=True)

            produto.save()
            instances.update({'produto': produto.instance})

        self.serializer.save()
        instances.update({'origem': self.serializer.instance})

        return instances
