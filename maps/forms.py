from django import forms

from .models import Shapefile, SvgFile


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
            "config",
            ]