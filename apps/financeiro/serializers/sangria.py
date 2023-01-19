from rest_framework import serializers
from ..models import Sangria


class SangriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sangria
        fields = '__all__'
