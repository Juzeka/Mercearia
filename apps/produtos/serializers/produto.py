from rest_framework import serializers
from ..models import ProdutoOrigem, Produto


class ProdutoOrigemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoOrigem
        fields = '__all__'


class ProdutoSerializer(ProdutoOrigemSerializer):
    class Meta:
        model = Produto
