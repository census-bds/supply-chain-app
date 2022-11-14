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

    def GD_object(self, geo = "national"):               
        geographylvl_exists = GeographyLevel.objects.filter(level=geo).exists()
        if geographylvl_exists:         
            geo_lvl = GeographyLevel.objects.get(level=geo)
        else: 
            geo_lvl = GeographyLevel(level=geo, meta_details = "").save()

        if geo == "national": 
            gd_dict = {
                'level': geo_lvl, 
                'zipcode' : "", 
                'fips_code' : "", 
                'geo_id' : "", 
                'port' : None, 
                'county' : "", 
                'state' : None, 
                'country' : "USA"
            }         
        # need to update this dictionary for county, port, state, zip levels    
        elif geo == "county": 
            gd_dict = {
                'level': geo_lvl, 
                'zipcode' : "", 
                'fips_code' : "", 
                'geo_id' : "", 
                'port' : None, 
                'county' : "", 
                'state' : None, 
                'country' : "USA"
            }      
        geo_detail_exists = GeographyDetail.objects.filter(
            level = gd_dict['level'], 
            zipcode = gd_dict['zipcode'], 
            fips_code = gd_dict['fips_code'], 
            geo_id = gd_dict['geo_id'], 
            port = gd_dict['port'], 
            county = gd_dict['country'], 
            state = gd_dict['state'], 
            country = gd_dict['country']
        ).exists()
        if not geo_detail_exists: 
                # gd = GeographyDetail(
                #     level = geo_lvl, 
                #     zipcode = gd_dict['zipcode'], 
                #     fips_code = gd_dict['fips_code'], 
                #     geo_id = gd_dict['geo_id'], 
                #     port = gd_dict['port'], 
                #     county = gd_dict['country'], 
                #     state = gd_dict['state'], 
                #     country = gd_dict['country']
                # ).save()
                # in case exact thing doesn't exist then check if there is a match 
                # if there is match on level, then update etc  
                gd, created = GeographyDetail.objects.update_or_create(
                    level = geo_lvl, 
                    defaults = gd_dict
                )
        else: 
            gd = GeographyDetail.objects.get(
                    level = geo_lvl, 
                    zipcode = gd_dict['zipcode'], 
                    fips_code = gd_dict['fips_code'], 
                    geo_id = gd_dict['geo_id'], 
                    port = gd_dict['port'], 
                    county = gd_dict['country'], 
                    state = gd_dict['state'], 
                    country = gd_dict['country']
                )

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
    def FT_objects(self, df, datetime_type, pd_code, pd_lvl): 
        all_ft_objects = []
        # not sure what is a good parameter for HS6... for the columns 
        for index, row in df.iterrows():
            import_val = row['import_value']
            export_val = row['export_value']
            datetime_val = row[datetime_type]
            pd_val_column = pd_code+pd_lvl
            hs6_val = row[pd_val_column.upper()] 

            pd = self.PD_object(pd_lvl, pd_code, hs6_val)
            gd = self.GD_object(None)

            ft_exists = ForeignTrade.objects.filter(
                geography = gd, 
                product_code_details = pd, 
                export_value = export_val, 
                import_value = import_val, 
                year = datetime_val if datetime_type == 'YEAR' else "",
                month = datetime_val if datetime_type == 'MONTH' else "",  
                datetime_type = datetime_type
            ).exists()
            if not ft_exists: 
                ft = ForeignTrade(
                    geography = gd, 
                    product_code_details = pd, 
                    export_value = export_val, 
                    import_value = import_val, 
                    year = datetime_val if datetime_type == 'YEAR' else "",
                    month = datetime_val if datetime_type == 'MONTH' else "",  
                    datetime_type = datetime_type
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
        # will want to customize this better for code, level, and datetime types & other params
        product_code = 'hs'
        product_lvl = '6'
        print(geo_df)
        # self.FT_objects(geo_df, 'YEAR', product_code, product_lvl)

