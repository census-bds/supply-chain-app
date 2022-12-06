from rest_framework import serializers
from .models import ForeignTrade, GeographyDetail, ProductCode

class GeographyDetailSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = GeographyDetail
        fields = '__all__'
class ProductCodeSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = ProductCode
        fields = '__all__'
class ForeignTradeSerializer(serializers.ModelSerializer):
    # reference serializers for foreign key fields 
    # if many to many, set many=True 
    # if want custom or particular field, example: field_name = serializers.RelatedField(source='field', read_only=True)

    geography = GeographyDetailSerializer()
    product_code_details = ProductCodeSerializer()
    class Meta:
        model = ForeignTrade
        fields = '__all__'