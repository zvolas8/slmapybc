from django.contrib import admin

# Register your models here.

from maps.models import Shapefile, SvgFile

admin.site.register(Shapefile)
admin.site.register(SvgFile)