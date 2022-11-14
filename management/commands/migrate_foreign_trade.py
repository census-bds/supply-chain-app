from django.core.management.base import BaseCommand, CommandError

from supply_chain_apis.data_source import IntlTrade
from datetime import datetime
from scip.models import ForeignTrade, GeographyDetail, ProductCode, ProductCodeDetail, GeographyLevel, ProductCodeType
# complete script 5/6/2021
class Command(BaseCommand):
    help = 'Migrate data'

    def add_arguments(self, parser):
        parser.add_argument('--d', default="", nargs="+", type=str)
#      import_value export_value  YEAR     HS6
# 0        89682644    186922035  2020  010121
# 1       458307529    108810155  2020  010129

    def GD_object(self, geo = None): 
        if geo == None: 
            geographylvl_exists = GeographyLevel.objects.filter(level="national", meta_details="").exists()
            if geographylvl_exists: 
                geo_lvl = GeographyLevel.objects.get(level="national", meta_details="")
                geo_detail_exists = GeographyDetail.objects.filter(level = geo_lvl).exists()
                if not geo_detail_exists: 
                    gd = GeographyDetail(
                        level = geo_lvl, 
                        # zipcode = "", 
                        # fips_code = "", 
                        # geo_id = "", 
                        # port = ", 
                        # county = "", 
                        # state = , 
                        # country = "USA"
                    ).save()
                else: 
                    gd = GeographyDetail.objects.get(level = geo_lvl)
        # else: 
        #     gd = GeographyDetail(

        #     )
        return gd
    def PD_object(self, level, type, val): 
        typee = ProductCodeType.objects.get(product_code_type=type)
        pd_detail_exists = ProductCodeDetail.objects.filter(product_code_type = typee, product_code_level = level).exists()
        if pd_detail_exists: 
            pd_detail = ProductCodeDetail.objects.get(
                    product_code_type = typee, 
                    product_code_level = level
                )
            pd_code_exists = ProductCode.objects.filter(
                product_name = "",
                product_code = val,
                product_code_detail = pd_detail
            ).exists()
            if pd_code_exists:
                pd = ProductCode.objects.get(
                    product_name = "",
                    product_code = val,
                    product_code_detail = pd_detail
                )
            else:  
                pd = ProductCode( 
                    product_name = "",
                    product_code = val,
                    product_code_detail = pd_detail
                ).save()
        return pd
    def FT_objects(self, df): 
        all_ft_objects = []
        # not sure what is a good parameter for HS6... for the columns 
        for index, row in df.iterrows():
            import_val = row['import_value']
            export_val = row['export_value']
            year_val = row['YEAR']
            hs6_val = row['HS6'] 

            pd = self.PD_object("6","hs", hs6_val)
            gd = self.GD_object(None)

            ft_exists = ForeignTrade.objects.filter(
                geography = gd, 
                product_code_details = pd, 
                export_value = export_val, 
                import_value = import_val, 
                year = year_val, 
                datetime_type = "year"
            ).exists()
            if not ft_exists: 
                ft = ForeignTrade(
                    geography = gd, 
                    product_code_details = pd, 
                    export_value = export_val, 
                    import_value = import_val, 
                    datetime = datetime.date(year_val),
                    datetime_type = "year"
                )
                all_ft_objects.append(ft)
        ForeignTrade.objects.bulk_create(all_ft_objects)


    def handle(self, *args, **options):
        print("handling")
        intlT = IntlTrade()
        # ['HS6']
        # initialize GeographyPort tables 
        # initialize GeographyState tables 
        geo_df = intlT.combine_geo()
        self.FT_objects(geo_df)

