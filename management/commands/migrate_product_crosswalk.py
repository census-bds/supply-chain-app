from django.core.management.base import BaseCommand, CommandError

from datetime import datetime
from scip.models import ProductCodeType, ProductCodeDetail, ProductCode, ProductCodeArchive, ProductCodeCrosswalk
import pandas as pd
from pathlib import Path

# should make admin be able to search through productcodes
# TODO: why are there product code duplicates?
# complete script 5/6/2021
# TODO: make sure when set product codes, you set them to integer not floats!
# make sure in foreign trade, you're creating product codes if they don't exist 
class Command(BaseCommand):
    help = 'Migrate data'

    def add_arguments(self, parser):
#         can pass in yml or file with state abbrev / state dict to get info from too 
        parser.add_argument('--d', default="", nargs="+", type=str)
        # 2022 updated hs codes sheet
        # - new hs is for 2022
        # - current hs is probably for 2017 
        # ranked by sctg5 & ranked by hs10
        # - all the hs is referencing NEW hs codes 
        # - DESCRIPT_L column is what 2022 updated hs codes is referencing
        parser.add_argument('--products', default ="../sc/scip/concordances/hs_sctg5_crosswalk_woah_ke_9.9.22.xlsx")


    def create_product_code_type(self, pd_type): 
        pd_type_exists = ProductCodeType.objects.filter(
            product_code_type = pd_type
        ).exists()
        if not pd_type_exists: 
            pd_type = ProductCodeType(
                product_code_type = pd_type
            ).save()
        else: 
            pd_type = ProductCodeType.objects.get(
                product_code_type = pd_type
            )
        return pd_type

    def create_product_code_detail(self, pd_type, pd_detail):
        pd_detail_exists = ProductCodeDetail.objects.filter(
            product_code_type = pd_type, 
            product_code_level = pd_detail, 
        ).exists()
        if not pd_detail_exists: 
            pd_detail = ProductCodeDetail(
                product_code_type = pd_type, 
                product_code_level = pd_detail, 
            ).save()
        else: 
            pd_detail = ProductCodeDetail.objects.get(
                product_code_type = pd_type, 
                product_code_level = pd_detail
            )
        return pd_detail
    
    def mapping_hs(self, df): 
        pd_type_char = "hs"
        pd_code_col_name = 'HS 10-digit'
        pd_code_flag_col = 'HS-flag'
        pd_code_level = '10'

        desc2_4_col = 'DESC2_4'
        descript_l_col = 'DESCRIPT_L'

        product_code_list = []
        pd_type_exists = ProductCodeType.objects.filter(product_code_type = pd_type_char).exists()
        if not pd_type_exists: 
            pd_type = self.create_product_code_type(pd_type_char)
        else: 
            pd_type = ProductCodeType.objects.get(
                product_code_type = pd_type_char
            )
        for index, row in df.iterrows(): 
            pd_code = row[pd_code_col_name]
            pd_code_flag = row[pd_code_flag_col]
            pd_code_descrip = row[descript_l_col]

            desc2_4 = row[desc2_4_col]
            descript = row[descript_l_col]

            pd_detail_exists = ProductCodeDetail.objects.filter(
                product_code_type = pd_type, 
                product_code_level = pd_code_level
            ).exists()
            if not pd_detail_exists: 
                pd_detail = self.create_product_code_detail(pd_type, pd_code_level)
            else: 
                # there should only be one. get rid of duplicates! 
                # if exists and more than 1, then delete the others; keep one 
                pd_detail = ProductCodeDetail.objects.filter(
                    product_code_type = pd_type, 
                    product_code_level = pd_code_level 
                ).first()
            
            pd_code_exists = ProductCode.objects.filter(
                # product_name = "", 
                product_code = pd_code, 
                # product_code_detail = pd_detail, 
                # description = pd_code_descrip, 
                # desc2_4 = desc2_4, 
                # descript_L = descript, 
                # flag = pd_code_flag, 
                # active = True, 
                # year = '2022', 
            ).exists()

            if not pd_code_exists: 
                product_code = ProductCode(
                    product_name = "", 
                    product_code = pd_code, 
                    product_code_detail = pd_detail, 
                    description = pd_code_descrip, 
                    desc2_4 = desc2_4, 
                    descript_L = descript, 
                    flag = pd_code_flag, 
                    active = True, 
                    year = '2017', 
                )
                product_code_list.append(product_code)
        print("finished mapping hs")
        return ProductCode.objects.bulk_create(product_code_list)

    def mapping_product_codes(self, 
        df, 
        pd_type_char, 
        pd_code_col_name, 
        pd_code_flag_col, 
        pd_code_descrip_col, 
        pd_code_level, 
        desc2_4_col, 
        descript_l_col): 

        product_code_list = []
        pd_type_exists = ProductCodeType.objects.filter(product_code_type = pd_type_char).exists()
        if not pd_type_exists: 
            pd_type = self.create_product_code_type(pd_type_char)
        else: 
            pd_type = ProductCodeType.objects.get(
                product_code_type = pd_type_char
            )
        for index, row in df.iterrows(): 
            pd_code = row[pd_code_col_name]
            pd_code_flag = row[pd_code_flag_col]
            pd_code_descrip = row[pd_code_descrip_col]
            desc2_4 = row[desc2_4_col] if desc2_4_col else ''
            descript = row[descript_l_col] if descript_l_col else ''

            pd_detail_exists = ProductCodeDetail.objects.filter(
                product_code_type = pd_type, 
                product_code_detail = pd_code_level
            ).exists()
            if not pd_detail_exists: 
                pd_detail = self.create_product_code_detail(pd_type, pd_code_level)
            else: 
                pd_detail = ProductCodeDetail.objects.get(
                    product_code_type = pd_type, 
                    product_code_detail = pd_code_level
                )
            
            pd_code_exists = ProductCode.objects.filter(
                # product_name = "", 
                product_code = pd_code, 
                # product_code_detail = pd_detail, 
                # description = pd_code_descrip, 
                # flag = pd_code_flag, 
                # desc2_4 = desc2_4, 
                # descript_L = descript, 
                # active = True, 
                # year = '2022', 
            ).exists()

            if not pd_code_exists: 
                product_code = ProductCode(
                    product_name = "", 
                    product_code = pd_code, 
                    product_code_detail = pd_detail, 
                    description = pd_code_descrip, 
                    flag = pd_code_flag, 
                    desc2_4 = desc2_4, 
                    descript_L = descript, 
                    active = True, 
                    year = '2017', 
                )
                product_code_list.append(product_code)
        print("finishing hs10")
        return ProductCode.objects.bulk_create(product_code_list)
    def mapping_sctg(self, df):
        pd_type_char = "sctg"
        pd_code_col_name = 'SCTG5-digit' 
        pd_code_flag_col = 'SCTG-flag'
        pd_code_descrip_col = 'SCTG-5-DIGITS Description' 
        pd_code_level = '5'

        product_code_list = []
        pd_type_exists = ProductCodeType.objects.filter(product_code_type = pd_type_char).exists()
        if not pd_type_exists: 
            pd_type = self.create_product_code_type(pd_type_char)
        else: 
            pd_type = ProductCodeType.objects.filter(
                product_code_type = pd_type_char
            ).first()
        for index, row in df.iterrows(): 
            pd_code = row[pd_code_col_name]
            pd_code_flag = row[pd_code_flag_col]
            pd_code_descrip = row[pd_code_descrip_col]

            pd_detail_exists = ProductCodeDetail.objects.filter(
                product_code_type = pd_type, 
                product_code_level = pd_code_level
            ).exists()
            if not pd_detail_exists: 
                pd_detail = self.create_product_code_detail(pd_type, pd_code_level)
            else: 
                pd_detail = ProductCodeDetail.objects.filter(
                    product_code_type = pd_type, 
                    product_code_level = pd_code_level
                ).first()
            
            pd_code_exists = ProductCode.objects.filter(
                # product_name = "", 
                product_code = pd_code, 
                # product_code_detail = pd_detail, 
                # description = pd_code_descrip, 
                # flag = pd_code_flag, 
                # active = True, 
                # year = '2022', 
            ).exists()

            if not pd_code_exists: 
                product_code = ProductCode(
                    product_name = "", 
                    product_code = pd_code, 
                    product_code_detail = pd_detail, 
                    description = pd_code_descrip, 
                    flag = pd_code_flag, 
                    active = True, 
                    year = '2017', 
                )
                product_code_list.append(product_code)
        print("finishing mapping sctg")
        return ProductCode.objects.bulk_create(product_code_list)

    def product_code_crosswalk(self, df): 
        pd_y_col = 'SCTG5-digit' 
        pd_x_col = 'HS 10-digit'
        crosswalk_list = []
        list_pdy_dne = []
        list_pdx_dne = []
        for index, row in df.iterrows(): 
            pd_y = row[pd_y_col]
            pd_x = row[pd_x_col]
            pd_code_y_exists = ProductCode.objects.filter(
                product_code = pd_y
            ).exists()
            pd_code_x_exists = ProductCode.objects.filter(
                product_code = pd_x
            ).exists()
            if pd_code_y_exists and pd_code_x_exists: 
                pd_y_val = ProductCode.objects.filter(
                    product_code = pd_y
                ).first()
                pd_x_val = ProductCode.objects.filter(
                    product_code = pd_x
                ).first()
                crosswalk_exists = ProductCodeCrosswalk.objects.filter(
                    product_code_x = pd_x_val, 
                    product_code_y = pd_y_val
                ).exists()
                if not crosswalk_exists: 
                    product_code_cross = ProductCodeCrosswalk(
                        product_code_x = pd_x_val, 
                        product_code_y = pd_y_val
                    )
                    crosswalk_list.append(product_code_cross)
            elif pd_code_y_exists: 
                pd_y_val = ProductCode.objects.filter(
                    product_code = pd_y
                ).first()
                list_pdy_dne.append(pd_y_val)
            elif pd_code_x_exists: 
                pd_x_val = ProductCode.objects.filter(
                    product_code = pd_x
                ).first()
                list_pdx_dne.append(pd_x_val)
            # else: 
            #     print("product cross walk doesn't map anything")
        # print("Prod x dne: ", list_pdx_dne)
        # print("Prod y dne: ", list_pdy_dne)
        print("finishing cross walk")
        return ProductCodeCrosswalk.objects.bulk_create(crosswalk_list)
    def update_product_mappings(self, df): 
        # df.keys() returns the sheets of an excel workbook 
        product_archive = []
        update_products = []
        pd_diff_current_desc = []
        for index, row in df.iterrows(): 
            current_hs = row['current hs']
            new_hs = row['new hs']
            current_hs_desc = row['description 1'] 
            new_hs_desc = row['description 2']

            product_code_exists = ProductCode.objects.filter(
                product_code = current_hs
            ).exists() 
            if product_code_exists: 
                pd = ProductCode.objects.get(
                    product_code = current_hs
                )
                    
                pd_name = pd.product_name
                pd_code = pd.product_code
                pd_code_detail = pd.product_code_detail
                desc = pd.description
                flag = pd.flag
                active = pd.active
                year = pd.year # double check this is 2017... 
                desc2_4 = pd.desc2_4
                descript_L = pd.descript_L
                if current_hs_desc != pd.description: 
                    pd_diff_current_desc.append(pd_code)
                pd_archive_exists = ProductCodeArchive.objects.filter(
                    product_name = pd_name, 
                    product_code = pd_code, 
                    product_code_detail = pd_code_detail, 
                    description = desc, # do we want to set the old desc or the current desc from the spreadsheet
                    flag = flag, 
                    active = active, 
                    year = year, # double check this is 2017... 
                    desc2_4 = desc2_4, 
                    descript_L = descript_L, 
                ).exists()
                if not pd_archive_exists: 
                    pd_archive = ProductCodeArchive(
                        product_name = pd_name, 
                        product_code = pd_code, 
                        product_code_detail = pd_code_detail, 
                        description = desc, # do we want to set the old desc or the current desc from the spreadsheet
                        flag = flag, 
                        active = active, 
                        year = year, # double check this is 2017... 
                        desc2_4 = desc2_4, 
                        descript_L = descript_L, 
                    ) 
                    product_archive.append(pd_archive)
            
            # create new product code if it doesn't exist; delete old one after archived 
                pd.product_code = new_hs
                pd.descript_L = new_hs_desc
                pd.year = "2022"
                update_products.append(pd)
        # print("Desc NM: ", pd_diff_current_desc)
        print("finishing up prod mappings")
        ProductCodeArchive.objects.bulk_create(product_archive)
        ProductCode.objects.bulk_update(update_products, ['product_code', 'descript_L', 'year'])


    def handle(self, *args, **options):
        if options['products']:
            data = Path(options['products']) # path based on system
        else:
            raise CommandError('Must pass in args for --excel')

        product_crosswalk_df = pd.read_excel(data, engine='openpyxl', sheet_name=None)
        df = product_crosswalk_df
        sctg5 = df['ranked by SCTG5']
        hs10 = df['ranked by HS10']
        hs10_crosswalk = df['2022 updated hs codes']
        
        pd_type_char = "sctg"
        pd_code_col_name = 'SCTG5-digit' 
        pd_code_flag_col = 'SCTG-flag'
        pd_code_descrip_col = 'SCTG-5-DIGITS Description' 
        pd_code_level = '5'
        
        pd_type_char = "hs"
        pd_code_col_name = 'HS 10-digit'
        pd_code_flag_col = 'HS-flag'
        pd_code_level = '10'
        pd_code_descrip_col = 'DESCRIPT_L'
        desc2_4_col = 'DESC2_4'
        descript_l_col = 'DESCRIPT_L'


        self.mapping_hs(hs10)
        self.mapping_sctg(sctg5)
        self.update_product_mappings(hs10_crosswalk)
        self.product_code_crosswalk(hs10)
        self.product_code_crosswalk(sctg5) # not sure complete diff between hs10 and sctg5, so might need to add source field...
