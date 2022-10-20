from django.db import models
from django.utils import timezone 

# Create your models here.

class ForeignTrade(models.Model): 
    geography = models.ForeignKey("GeographyDetail", on_delete = models.CASCADE)
    product_code_details = models.ForeignKey("ProductCodeDetail", on_delete = models.CASCADE)
    export_value = models.CharField(max_length = 255, default ="")
    import_value = models.CharField(max_length = 255, default ="")
    year = models.CharField(max_length = 255, default = "")


