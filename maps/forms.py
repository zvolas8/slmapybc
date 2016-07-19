from django import forms

from .models import Shapefile, SvgFile, Layers


class ShapefileForm(forms.ModelForm):
    class Meta:
        model = Shapefile
        fields = [
            "name",
            "shapefileName",
            "fileshp",
            "layerName",
            ]

class SvgForm(forms.ModelForm):
    class Meta:
        model = SvgFile
        fields = [
            "name",
            #"config",
            ]

class LayersForm(forms.ModelForm):
    class Meta:
        model = Layers
        fields = [
            "idLayer",
            "name",
            ]