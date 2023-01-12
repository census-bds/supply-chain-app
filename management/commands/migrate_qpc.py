from django.core.management.base import BaseCommand, CommandError

from supply_chain_apis.qpc import QPC
from datetime import datetime
import openpyxl
# from scip.models import .
# complete script 5/6/2021
class Command(BaseCommand):
    help = 'Migrate data'

    def add_arguments(self, parser):
        parser.add_argument('--d', default="", nargs="+", type=str)

    def migrate_qpc_dfs(self, dfs): 
        qpcs = []
        for (label, df) in dfs: 
            print(label)
            print(df.head())
            qpc = QPC(
                naics_code = df['NAICS Code(s)'], 
                description = df['Description'], 
                industry_coverage_lt50 = df['Industry Coverage LT 50p'], 
                utilization_rate = df['Utilization Rate '], 
                standard_error = df['Standard Error '], 
                industry_coverage_lt50_p1 = df['Average Plant hours per week in operation  '], 
                standard_error_p1 = df['Standard Error .1'], 
                utilization_rate_p1 = df['Average Plant hours per week in operation  .1']
            )
            qpcs.append(qpc)

        QPC.objects.bulk_create(qpcs)
        
    def handle(self, *args, **options):
        print("handling")
        qpc = QPC()
        urls = qpc.generate_urls()
        dfs = qpc.clean_qpc_file(urls) 
        self.migrate_qpc_dfs(dfs)