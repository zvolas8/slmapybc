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
    svg_final_list,
    add_layer,
    remove_layer_list,
    delete_layer,
    svgToFinalSvg,
    mapsSettings,
    SettingsLayer,
    SettingsLayerEdit,
    SettingsLayerAdd,
    )

urlpatterns = [
    url(r'^shplist/$', shapefile_list, name='shplist'),
    url(r'^svglist/$', svg_list, name='svglist'),
    url(r'^svgfinallist/$', svg_final_list, name='svgfinallist'),
    url(r'^createshp/$', maps_create, name='createshp'),
    url(r'^createsvg/$', maps_createsvg, name='createsvg'),
    url(r'^(?P<id>\d+)/delete/$', delete_svg),
    url(r'^(?P<id>\d+)/addLayer/$', add_layer),
    url(r'^(?P<id>\d+)/deleteLayer/(?P<layer>\w+)/$', delete_layer, name='deletelayer'),
    url(r'^(?P<id>\d+)/removeLayer/$', remove_layer_list),
    url(r'^(?P<id>\d+)/$', svg_detail, name='svgdetail'),
    url(r'^(?P<id>\d+)/edit/$', update_svg, name='svgupdate'),
    url(r'^(?P<id>\d+)/translate/$', translation_word, name='svgtranslate'),
    url(r'^(?P<id>\d+)/toFinal/$', svgToFinalSvg),
    url(r'^mapssettings/$', mapsSettings, name='mapssettings'),
    url(r'^mapssettings/layer$', SettingsLayer, name='settingsLayer'),
    url(r'^mapssettings/layer/add$', SettingsLayerAdd, name='settingsLayerAdd'),
    url(r'^mapssettings/layer/(?P<id>\d+)/edit/$', SettingsLayerEdit, name='settingsLayerEdit'),
]