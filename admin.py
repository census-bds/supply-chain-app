from django.contrib import admin

# Register your models here.
from .models.general import GeographyLevel, GeographyPort, GeographyState, GeoId, ProductCodeType, ProductCodeDetail, ProductCode, ProductCodeArchive
from .models.foreigntrade import ForeignTrade

# ==> geography 
admin.site.register( GeographyLevel )
admin.site.register( GeographyPort )
admin.site.register( GeographyState )
admin.site.register( GeoId )

# ==> product codes
admin.site.register( ProductCode )
admin.site.register( ProductCodeArchive )
admin.site.register( ProductCodeType )
admin.site.register( ProductCodeDetail )

# ==> foreign trade data  
admin.site.register( ForeignTrade )

