from django.contrib import admin

# Register your models here.
from .models.general import GeographyLevel, GeographyPort, GeographyState, GeographyDetail, ProductCodeType, ProductCodeDetail
from .models.foreigntrade import ForeignTrade

# ==> geography 
admin.site.register( GeographyLevel )
admin.site.register( GeographyPort )
admin.site.register( GeographyState )
admin.site.register( GeographyDetail )

# ==> product codes
admin.site.register( ProductCodeType )
admin.site.register( ProductCodeDetail )

# ==> foreign trade data  
admin.site.register( ForeignTrade )
