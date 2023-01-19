from apps.produtos.serializers import (
    ProdutoSerializer,
    ProdutoOrigemSerializer
)


class ProdutoServices:
    def __init__(self, *args, **kwargs):
        self.data = kwargs.get('data')
        self.serializer = kwargs.get('serializer')

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
