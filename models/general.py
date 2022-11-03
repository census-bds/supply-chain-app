from django.db import models
from django.utils import timezone 

# Create your models here.

class GeographyLevel(models.Model): 
    # example: zip, county, port, state, national; required 
    level = models.CharField(max_length=255, default ="")
    meta_details = models.CharField(max_length=255, default="")

class GeographyPort(models.Model): 
    port = models.CharField(max_length=255, default="")
    port_name = models.CharField(max_length=255, default="")

class GeographyState(models.Model): 
    state = models.CharField(max_length=255, default="")
    state_abbreviation = models.CharField(max_length=255, default="")

class GeographyDetail(models.Model): 
    level = models.ForeignKey("GeographyLevel", on_delete = models.CASCADE) 
    zipcode = models.CharField(max_length=255, default="")
    fips_code = models.CharField(max_length=255, default="")
    geo_id = models.CharField(max_length=255, default="")
    port = models.ForeignKey("GeographyPort", on_delete = models.CASCADE, null = True)
    county = models.CharField(max_length=255, default="")
    state = models.ForeignKey("GeographyState", on_delete = models.CASCADE, null = True)
    country = models.CharField(max_length=255, default="USA")

class ProductCodeType(models.Model): 
    # 'hs', 'sctg', 'napcs', 'sitc', etc 
    product_code_type = models.CharField(max_length=255, default="")

class ProductCodeDetail(models.Model): 
    product_code_type = models.ForeignKey("ProductCodeType", on_delete = models.CASCADE)
    product_code_level = models.CharField(max_length=255, default="")
    
class ProductCode(models.Model): 
    product_name =  models.CharField(max_length=255, default="")
    product_code = models.CharField(max_length=255, default = "")
    product_code_detail = models.ForeignKey("ProductCodeDetail", on_delete = models.CASCADE)
