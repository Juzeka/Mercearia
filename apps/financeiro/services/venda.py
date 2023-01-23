from apps.produtos.models import ProdutoOrigem, Produto
from apps.produtos.serializers import ProdutoOrigemSerializer


class VendaServices:
    def __init__(self, *args, **kwargs):
        self.data = kwargs.get('data')

    def has_origem(self):
        origem = self.data.get('produto_origem', False)
        return True if origem else False

    def get_produto_origem(self):
        if self.has_origem():
            return ProdutoOrigem.objects.filter(
                    pk=self.data.get('produto_origem')
                )

    def nao_existe_produto_origem(self):
        origem = self.has_origem()

        return self.get_produto_origem().exists() if origem else False

    def get_produto(self):
        origem = self.get_produto_origem()

        return Produto.objects.get(origem=origem.first().pk) if origem else False

    def verificar_quantidade(self, produto):
        if not self.has_origem():
            return False

        return produto.quantidade - self.data.get('quantidade')

    def atualizar_estoque(self, produto):
        has_quantidade = self.verificar_quantidade(produto)
        data_produto = {'quantidade': has_quantidade}

        if data_produto.get('produto_origem'):
            data_produto.pop('produto_origem')
        if has_quantidade == 0:
            data_produto.update({'ativo': False})

        produto_serializer = ProdutoOrigemSerializer(
            produto,
            data=data_produto,
            partial=True
        )

        produto_serializer.is_valid(raise_exception=True)
        produto_serializer.save()
