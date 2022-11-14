from django.shortcuts import render
from rest_framework import viewsets
from scip.serializers import ForeignTradeSerializer
from scip.models import ForeignTrade
# Create your views here.
class ForeignTradeViewset(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing foreign trade data.
    """
    serializer_class = ForeignTradeSerializer
    queryset = ForeignTrade.objects.all()