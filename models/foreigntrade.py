from django.db import models
from django.utils import timezone 

# Create your models here.

class ForeignTrade(models.Model): 
    geography = models.ForeignKey("GeographyDetail", on_delete = models.CASCADE, null = True)
    product_code_details = models.ForeignKey("ProductCode", on_delete = models.CASCADE, null = True)
    export_value = models.PositiveIntegerField()
    import_value = models.PositiveIntegerField()
    # year = models.CharField(max_length = 255, default = "")
    # month = models.Date
    year = models.CharField(max_length = 255, default="")
    month = models.CharField(max_length = 255, default="")
    # datetime = models.DateTimeField(blank = True, null = True)
    datetime_type = models.CharField(max_length = 255, default ="")

