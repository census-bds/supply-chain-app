from django.contrib import admin

# Register your models here.
from .models import Product, Industry, Naics, NaicsEstablishmentsState, ProductCode

# ==> default admin registration
#admin.site.register( Activity )
admin.site.register( Product )
admin.site.register( ProductCode )

admin.site.register( Industry )
admin.site.register( Naics )
admin.site.register( NaicsEstablishmentsState )
