from django.conf.urls import url
from django.contrib import admin

from .views import (
    shapefile_list,
    maps_create,
    maps_createsvg,
    delete_svg,
    svg_list,
    svg_detail,
    update_svg,
    translation_word,
    )

urlpatterns = [
    url(r'^shplist/$', shapefile_list, name='shplist'),
    url(r'^list/$', svg_list, name='svglist'),
    url(r'^createshp/$', maps_create, name='createshp'),
    url(r'^createsvg/$', maps_createsvg, name='createsvg'),
    url(r'^(?P<id>\d+)/delete/$', delete_svg),
    url(r'^(?P<id>\d+)/$', svg_detail, name='svgdetail'),
    url(r'^(?P<id>\d+)/edit/$', update_svg, name='svgupdate'),
    url(r'^(?P<id>\d+)/translate/$', translation_word, name='svgtranslate'),
]