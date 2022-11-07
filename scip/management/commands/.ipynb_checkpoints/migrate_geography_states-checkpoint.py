from django.core.management.base import BaseCommand, CommandError

from supply_chain_apis.data_source import IntlTrade
from datetime import datetime
from scip.models import GeographyState
# complete script 5/6/2021
class Command(BaseCommand):
    help = 'Migrate data'

    def add_arguments(self, parser):
#         can pass in yml or file with state abbrev / state dict to get info from too 
        parser.add_argument('--d', default="", nargs="+", type=str)

    # need list of territories too?
    # only initializing states right now 
    
    def initialize_states(self, state_abbrev, state_dict): 
        gs_bulk = []
        for abbrev in state_abbrev: 
            state_val = state_dict[abbrev]
            gs_exists = GeographyState.objects.filter(state=state_val).exists() 
            if not gs_exists: 
                gs = GeographyState(
                    state = state_val, 
                    state_abbreviation = abbrev 
                )
                gs_bulk.append(gs) 
        return GeographyState.objects.bulk_create(gs_bulk) 


    def handle(self, *args, **options):
        state_abbrev = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
        state_dict = {"AL":"Alabama", 
                  "AK":"Alaska", 
                  "AZ":"Arizona", 
                  "AR":"Arkansas", 
                  "CA":"California", 
                  "CO":"Colorado", 
                  "CT":"Connecticut", 
                  "DC":"Washington D.C.", 
                  "DE":"Delaware", 
                  "FL":"Florida", 
                  "GA":"Georgia", 
                  "HI":"Hawaii", 
                  "ID":"Idaho", 
                  "IL":"Illinois", 
                  "IN":"Indiana", 
                  "IA":"Iowa", 
                  "KS":"Kansas", 
                  "KY":"Kentucky", 
                  "LA":"Louisiana", 
                  "ME":"Maine", 
                  "MD":"Maryland", 
                  "MA":"Massachusetts", 
                  "MI":"Michigan", 
                  "MN":"Minnesota", 
                  "MS":"Mississippi", 
                  "MO":"Missouri", 
                  "MT":"Montana", 
                  "NE":"Nebraska", 
                  "NV":"Nevada", 
                  "NH":"New Hampshire", 
                  "NJ":"New Jersey", 
                  "NM":"New Mexico", 
                  "NY":"New York", 
                  "NC":"North Carolina", 
                  "ND":"North Dakota", 
                  "OH":"Ohio", 
                  "OK":"Oklahoma", 
                  "OR":"Oregon", 
                  "PA":"Pennsylvania", 
                  "RI":"Rhode Island", 
                  "SC":"South Carolina", 
                  "SD":"South Dakota", 
                  "TN":"Tennessee", 
                  "TX":"Texas", 
                  "UT":"Utah", 
                  "VT":"Vermont", 
                  "VA":"Virginia", 
                  "WA":"Washington", 
                  "WV":"West Virginia", 
                  "WI":"Wisconsin", 
                  "WY":"Wyoming"
                  }
        self.initialize_states(state_abbrev, state_dict)
