from django.core.management.base import BaseCommand, CommandError

from datetime import datetime
from scip.models import GeographyLevel
# complete script 5/6/2021
class Command(BaseCommand):
    help = 'Migrate data'

    def add_arguments(self, parser):
#         can pass in yml or file with state abbrev / state dict to get info from too 
        parser.add_argument('--d', default="", nargs="+", type=str)

    def initialize_geo_levels(self, levels): 
        gl_bulk = []
        for level in levels: 
            gl_exists = GeographyLevel.objects.filter(level=level, meta_details="").exists()
            if not gl_exists: 
                gl = GeographyLevel(
                    level = level, 
                    meta_details = ""
                )
                gl_bulk.append(gl)
        return GeographyLevel.objects.bulk_create(gl_bulk)
     
    def handle(self, *args, **options):
        geo_levels = ["national", "zip", "county", "port", "state"]

        
        self.initialize_geo_levels(geo_levels)
