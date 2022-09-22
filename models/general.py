from django.db import models
from django.utils import timezone 

# Create your models here.

class Naics(models.Model): 
    naics_id = models.PositiveIntegerField()
    # i.e. manufacturing dry, condensed, and evaporated milk and dairy substitute
    description = models.CharField(max_length=255)
    firms_total = models.PositiveIntegerField(null=True)
    establishments_total = models.PositiveIntegerField(null=True)
    industry_concentration = models.PositiveIntegerField(null=True)
    domestic_mfg_capacity_per = models.PositiveIntegerField(null=True)
    total_val_domestic_prod_per = models.PositiveIntegerField(null=True)
    establishments_by_state = models.PositiveIntegerField(null=True)

# do we get establishment information or do we just get the number from cbp?
class NaicsEstablishmentsState(models.Model): 
    naics = models.ForeignKey('Naics', on_delete = models.CASCADE, null = True)
    establishments = models.PositiveIntegerField(null=True) # if we get est info, we might just want to do a many to many field to establishment model and get length
    state = models.CharField(max_length=255, blank=True, null=True)

class Product(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    total_value_imported = models.PositiveIntegerField(null=True)
    importing_firms = models.PositiveIntegerField(null=True)
    # use this as foreign key to get naics id and also can get length 
    importing_firms_naics = models.ManyToManyField('Naics', related_name="importing_firms", null = True)
    total_produced_domestic = models.PositiveIntegerField(null=True)
    total_value_exported = models.PositiveIntegerField(null=True)
    # relevant naics -- 
    manufacturing_naics = models.ManyToManyField('Naics', related_name="manufacturing", null = True)
    product_codes = models.ManyToManyField('ProductCode', related_name="product_codes", null= True)
class ProductCode(models.Model): 
    # detailed hs code from usaid 
    code = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
class Industry(models.Model): 
    name = models.CharField(max_length=255, blank=True, null=True)

class NaicsConcordance(models.Model): 
    year = models.PositiveIntegerField(null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    # harmonized system -- HS code; product & commodity codes need to be harmonized