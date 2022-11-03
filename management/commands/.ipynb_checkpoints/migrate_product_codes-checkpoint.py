from django.core.management.base import BaseCommand, CommandError

from datetime import datetime
from scip.models import ProductCodeType, ProductCodeDetail
# complete script 5/6/2021
class Command(BaseCommand):
    help = 'Migrate data'

    def add_arguments(self, parser):
#         can pass in yml or file with state abbrev / state dict to get info from too 
        parser.add_argument('--d', default="", nargs="+", type=str)

    def initialize_productcodetype(self, product_types): 
        pd_type_bulk = []
        for pd_type in product_types: 
            pd_type_exists = ProductCodeType.objects.filter(product_code_type=pd_type).exists() 
            if not pd_type_exists: 
                pd_type_obj = ProductCodeType(
                    product_code_type = pd_type
                )
                pd_type_bulk.append(pd_type_obj) 
        return ProductCodeType.objects.bulk_create(pd_type_bulk) 
    def initialize_productcodedetail(self, types, levels): 
        pd_code_detail_bulk = []
        for typee in types: 
            if typee in levels.keys(): 
                num_lev = levels[typee]
                pd_type_exists = ProductCodeType.objects.filter(product_code_type=typee).exists() 
                if pd_type_exists: 
                    for i in range(0, num_lev):
                        pd_d = ProductCodeDetail(
                            product_code_type = ProductCodeType.objects.get(product_code_type=typee), 
                            product_code_level = i+1
                        )
                        pd_code_detail_bulk.append(pd_d) 
        return ProductCodeDetail.objects.bulk_create(pd_code_detail_bulk) 
    def handle(self, *args, **options):
        product_types = ["hs", "sctg", "napcs", "sitc"]
        product_code_d = {
            "hs": 10
        }
        
        self.initialize_productcodetype(product_types)
        self.initialize_productcodedetail(product_types, product_code_d) 
