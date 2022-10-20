from django.core.management.base import BaseCommand, CommandError

from supply_chain_apis.data_source import IntlTrade
# complete script 5/6/2021
class Command(BaseCommand):
    help = 'Migrate data'

    def add_arguments(self, parser):
        parser.add_argument('--researchDb', default="", nargs="+", type=str)

    
    def handle(self, *args, **options):
        print("handling")
        intlT = IntlTrade()
        intlT.combine_geo()
