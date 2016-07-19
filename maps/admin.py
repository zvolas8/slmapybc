from django.contrib import admin

# Register your models here.

from maps.models import Shapefile, SvgFile, Layers

admin.site.register(Shapefile)
admin.site.register(SvgFile)
admin.site.register(Layers) 