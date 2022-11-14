from rest_framework import serializers
from scip.models import ForeignTrade
class ForeignTradeSerializer(serializers.Serializer):
    class Meta:
        model = ForeignTrade
        fields = '__all__'