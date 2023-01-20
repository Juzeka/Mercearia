from rest_framework import serializers
from ..models import Venda, ItemVenda


class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'


class ItemVendaSerializer(VendaSerializer):
    class Meta(VendaSerializer.Meta):
        model = ItemVenda
