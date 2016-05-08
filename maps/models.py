from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

def uploadLocation(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Shapefile(models.Model):

    LAYER_CHOICES = (
        ('state', 'Staty'),
        ('state-by-city', 'Staty skrze hlavni mesta'),
        ('region', 'Regiony'),
        ('province', 'Provincie'),
        ('region_cz', 'Kraje'),
        ('region_it', 'Oblasti'),
        ('autonomous_Comunity', 'Autonomni spolecenstvi'),
        ('bundesland', 'Spolkove zeme'),
        ('city', 'Mesta'),
        ('city-by-state', 'Hlavni mesta skrze staty'),
        ('river', 'Reky'),
        ('reservoir', 'Vodni nadrze'),
        ('lake', 'Jezera'),
        ('sea', 'More'),
        ('mountains', 'Pohori'),
        ('surface', 'Povrch'),
        ('island', 'Ostrovy'),
    )

    name = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    shapefileName = models.CharField(max_length=120, blank=True, null=True)
    fileshp = models.FileField(upload_to=uploadLocation, null=True, blank=True)
    #layerName = models.CharField(max_length=120, blank=True, null=True)
    layerName =  models.CharField(max_length=120, choices=LAYER_CHOICES)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("maps:shpdetail", kwargs={"id": self.id})

class SvgFile(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    config = models.TextField()
    filesvg = models.FileField(upload_to=uploadLocation, null=True, blank=True)
    pathToFileSvg = models.CharField(max_length=1024, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("maps:svgdetail", kwargs={"id": self.id})