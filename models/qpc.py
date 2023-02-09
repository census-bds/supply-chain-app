from django.db import models
from django.utils import timezone 

# Create your models here.

class QPC(models.Model): 
    # do my best either with partial concordances and descriptions etc 
    naics_code = models.CharField(max_length = 255, default="")
    description = models.CharField(max_length = 255, default="")
    industry_coverage_lt50 = models.CharField(max_length = 255, default="")
    utilization_rate = models.CharField(max_length = 255, default="")
    standard_error = models.CharField(max_length = 255, default="")
    industry_coverage_lt50_p1 = models.CharField(max_length = 255, default="")
    standard_error_p1 = models.CharField(max_length = 255, default="")
    utilization_rate_p1 = models.CharField(max_length = 255, default="")

