from django.db import models
from django.utils import timezone 
from django.core.validators import MaxValueValidator, MinValueValidator 

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

class GeoId(models.Model): 
    # geoid captures geo level 
    geoid_value = models.CharField(max_length=255, default="")
    # port = models.CharField(max_length=255, default="")
    # state = models.CharField(max_length=255, default="")
    level = models.ForeignKey("GeographyLevel", on_delete = models.CASCADE, null = True) 

# class GeographyDetail(models.Model): 
#     geo = models.ForeignKey("GeoId", on_delete = models.CASCADE, null=True)

class ProductCodeType(models.Model): 
    # 'hs', 'sctg', 'napcs', 'sitc', etc 
    product_code_type = models.CharField(max_length=255, default="")

class ProductCodeDetail(models.Model): 
    product_code_type = models.ForeignKey("ProductCodeType", on_delete = models.CASCADE)
    # is level same as flag? 
    product_code_level = models.CharField(max_length=255, default="")
    
class ProductCode(models.Model): 
    product_name =  models.CharField(max_length=255, default="")
    product_code = models.CharField(max_length=255, default = "")
    product_code_detail = models.ForeignKey("ProductCodeDetail", on_delete = models.CASCADE)
    # get from updated hs codes sheet since only one description - looks like it's DESCRIPT_L
    # do I need to do a table with descriptions for each code and assign the active one as foreign key?
    description = models.TextField(default="")
    active = models.BooleanField(default = False)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)], null = True)
    desc2_4 = models.TextField(default="", null = True)
    descript_L = models.TextField(default="", null = True)
    flag = models.CharField(default="", max_length=255)

class ProductCodeCrosswalk(models.Model): 
    product_code_x = models.ForeignKey("ProductCode", related_name="product_code_x", on_delete = models.CASCADE, null = True)
    product_code_y = models.ForeignKey("ProductCode", related_name="product_code_y", on_delete = models.CASCADE, null = True)

# prevent slow querying of the product code table by separating old data into an archive
class ProductCodeArchive(models.Model): 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    product_name =  models.CharField(max_length=255, default="")
    product_code = models.CharField(max_length=255, default = "")
    product_code_detail = models.ForeignKey("ProductCodeDetail", on_delete = models.CASCADE)
    description = models.TextField(default="")
    flag = models.CharField(max_length = 255, default = "")
    active = models.BooleanField(default = False)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)], null = True)
    desc2_4 = models.TextField(default="", null = True)
    descript_L = models.TextField(default="", null = True)
