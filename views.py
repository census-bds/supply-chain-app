from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ForeignTradeSerializer
from .models import ForeignTrade

from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Create your views here.
@method_decorator(name="list", decorator=swagger_auto_schema(
    operation_description = "Get all Issues, filtered by query parameters",
    # manual_parameters=[
    #     openapi.Parameter('geography', openapi.IN_QUERY, required=False, description="An integer value identifying specific Issue.", type=openapi.TYPE_INTEGER),
    #     openapi.Parameter('export_value', openapi.IN_QUERY, required=False, description="An integer value identifying specific Project.", type=openapi.TYPE_INTEGER)
    # ]
))
class ForeignTradeViewset(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing foreign trade data.
    """
    serializer_class = ForeignTradeSerializer
    queryset = ForeignTrade.objects.all()
    
    def get_queryset(self): 
        queryset = self.queryset     

        # id = self.request.query_params.get("id", None)

        # if id: 
        #     queryset.filter(id=id) 
        print('queryset', queryset)
        return queryset
