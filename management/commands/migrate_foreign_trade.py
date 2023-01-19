from django.core.management.base import BaseCommand, CommandError
from supply_chain_apis.intltrade import IntlTrade
from supply_chain_apis.exceptions import RequestBlankException
from datetime import datetime
from scip.models import ForeignTrade, GeographyDetail, ProductCode, ProductCodeDetail, GeographyLevel, ProductCodeType, GeoId
# complete script 5/6/2021
class Command(BaseCommand):
    help = 'Migrate data'

    def add_arguments(self, parser):
        parser.add_argument('--d', default="", nargs="+", type=str)
#      import_value export_value  YEAR     HS6
# 0        89682644    186922035  2020  010121
# 1       458307529    108810155  2020  010129

    def GD_object(self, geo, geo_id, geo_val):               
        geographylvl_exists = GeographyLevel.objects.filter(level=geo).exists()
        if geographylvl_exists:         
            geo_lvl = GeographyLevel.objects.get(level=geo)
        else: 
            geo_lvl = GeographyLevel(level=geo, meta_details = "").save()
    
        # need to update this dictionary for county, port, state, zip levels   
        # we will have a geography concordance/crosswalk using gis after shapefiles with overlapping geos 
        # keep geo meta data simple --> everything will be in geo id and links to census tiger which has the shape files 
        # just have geo id and level 
        # TODO: need to migrate into relevant geo id info -- tiger shapefile 
        # https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
        # will want to create a new geo id model 

        # TODO: creating new geoid objects for every geo detail object
        # will want to have another script cleaning up all these geo detail objects when we get geo ids...
        if geo_id: 
            geo_id_ref = GeoId.objects.get(
                geoid_value = geo_id

            )
        else: 
            # TODO might want to clean up this part -- seems repetitive with "port", "state" if/else statements
            if geo == "port": 
                geo_id_exists = GeoId.objects.filter(
                    port = geo_val
                ).exists()
                if not geo_id_exists: 
                    geo_id_ref = GeoId(
                        port = geo_val 
                    ).save()
                else: 
                    geo_id_ref = GeoId.objects.get(
                        port = geo_val
                    )
            elif geo == "state": 
                geo_id_exists = GeoId.objects.filter(
                    state = geo_val
                ).exists()
                if not geo_id_exists: 
                    geo_id_ref = GeoId(
                        state = geo_val
                    ).save()
                else: 
                    geo_id_ref = GeoId.objects.get(
                        state = geo_val 
                    )
            else: 
                geo_id_ref = None

        geo_detail_exists = GeographyDetail.objects.filter(
            level = geo_lvl, 
            geo = geo_id_ref
        ).exists()
        if not geo_detail_exists: 
                # in case exact thing doesn't exist then check if there is a match 
                # if there is match on level, then update etc  
                gd, created = GeographyDetail.objects.update_or_create(
                    level = geo_lvl, 
                    geo = geo_id_ref
                )
        else: 
            gd = GeographyDetail.objects.get(
                    level = geo_lvl, 
                    geo = geo_id_ref
            )

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
    def FT_objects(self, df, geo, datetime_type, pd_code, pd_lvl): 
        all_ft_objects = []
        # not sure what is a good parameter for HS6... for the columns 
        for index, row in df.iterrows():
            import_val = row['import_value']
            export_val = row['export_value']
            geo_val = row[geo] if geo else None
            datetime_val = row[datetime_type]
            pd_val_column = pd_code+pd_lvl
            hs6_val = row[pd_val_column.upper()] 

            pd = self.PD_object(pd_lvl, pd_code, hs6_val)
            # TODO will eventually want to get geo_id 
            gd = self.GD_object(geo, None, geo_val) #TO DO: add geo param to FT_objects

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
        hs_codes = ['HS2', 'HS4', 'HS6', 'HS10']
        geos = ['state', 'port', None]
        datetypes = ['month', 'year']
        for hs in hs_codes:
            for geo in geos:
                for d in datetypes:
                    try:
                        df = intlT.combine_geo(geo=geo, hs=hs, datetype=d)
                    except RequestBlankException:
                        continue
                    #TO DO: pass exception if invalid call
                    product_lvl = hs[2:]
                    print("data frame: ", df)
                    self.FT_objects(
                        df, 
                        geo, 
                        'YEAR' if d == 'year' else 'MONTH', 
                        'hs', 
                        product_lvl
                    )

