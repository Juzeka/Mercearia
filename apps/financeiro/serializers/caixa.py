from rest_framework import serializers
from ..models import Caixa


class CaixaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caixa
        fields = '__all__'
        depth = 2
