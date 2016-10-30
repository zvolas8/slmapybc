# -*- coding: utf-8 -*-

import os
import shutil
import re
import ast
import polib
import requests
import json
import csv
import codecs

csv.register_dialect(
            'mydialect',
            delimiter = ',',
            quotechar = '"',
            doublequote = True,
            skipinitialspace = True,
            lineterminator = '\r\n',
            quoting = csv.QUOTE_MINIMAL)

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from kartograph import Kartograph

from slugify import slugify

from lxml import etree

# Create your views here.

from .forms import ShapefileForm, SvgForm, LayersForm
from .models import Shapefile, SvgFile, Layers, Config
from django.conf import settings


def main_page(request):
    context = {}
    return render(request, "main_page.html", context)


def maps_create(request):
    form = ShapefileForm(request.POST or None, request.FILES or None)
    print form.errors
    print form.is_valid()
    if form.is_valid():
        file = form.save(commit=False)
        shpName = form.cleaned_data['name']
        layerName = form.cleaned_data['layerName']
        #layerName2 = form.cleaned_data['layerName2']
        #layersObject = get_object_or_404(Layers, id=layerName2.id)
        #file.layerName2 = layersObject

        tempConfig = request.POST['configArea'] 
        file.name = shpName
        for f in request.FILES.getlist('files'):
            if f.name[-3:] == "shp":
                file.shapefileName = f.name
                file.fileshp = f
                tempfile = f  

        file.save()

        instance = form.save(commit=False);
        instance.fileshp = tempfile
        instance.save()

        for f in request.FILES.getlist('files'):
            if f.name[-3:] != "shp":
                path = default_storage.save(os.path.join(settings.MEDIA_ROOT, str(instance.id), f.name), ContentFile(f.read()))

        

        
        


        #    pr = transifexCreateNewProject(projectName)
        #    print pr
        #    re = transifexCreateNewResource(resName, projectName)
        #    print re

        #config = create_config(instance.id, tempfile.name, layerName)
        config = addSrcToConfig(tempConfig, instance.id, tempfile.name)
        svgId = save_svg(config, shpName)
        svgWords = getAllWordsForSvg(getFilepathBySvgId(svgId))
        sourceWords = getSourceStringForTranslate(svgWords)
        addWordsToSourceCSV(sourceWords, svgWords)
        
        resName = getResourceName()
        projectName = getProjectName()

        re = transifexCreateNewResource(resName, projectName)
        print re

        #transifexUpdateResource(resName, projectName)

        deleteFolder = os.path.join(settings.MEDIA_ROOT, "None") 
        shutil.rmtree(deleteFolder)

        messages.success(request, "shapefile byl ulozen")

    ConfigForPost = json.dumps(config_for_post())
    layers = Layers.objects.all()
    context = {
        "layers": layers,
        "config": ConfigForPost,
        "form": form
        }
    return render(request, "shapefile_form.html", context)

def getResourceName():
    return "translations_cs" 

def getProjectName():
    return "bakalarskaprace"

def save_svg(config, name):
    svg = SvgFile()
    tName =  os.path.splitext(name)[0]
    tConfig = create_config_format(config)
    svg.name = name
    svg.config = tConfig
    svg.isOld = False
    svg.save()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join("img", str(svg.id), tName + ".svg")
    svg.pathToFileSvg = path
    svg.save()
    create_svg_file(config, name, svg.id)
    return svg.id

def create_config_format(config):
    c = config['layers']
    return c

def addSrcToConfig(config, id, FILE_NAME):
    config = dictFromString(config)
    config['layers'][0]['src'] =  os.path.join(settings.MEDIA_ROOT, str(id), FILE_NAME)
    return config

def addSrcToConfigDict(config, id, FILE_NAME):
    config['layers'][0]['src'] =  os.path.join(settings.MEDIA_ROOT, str(id), FILE_NAME)
    return config

#def create_config(id, FILE_NAME, layerName):

#    config = {
#            "layers": [{
#                "id": str(layerName),
#                "src": os.path.join(settings.MEDIA_ROOT, str(id), FILE_NAME),
#                "attributes": {
#                    "id": "iso_a2",
#                    "code": "name",
#                    "name": "name"
#                }
#            }]
#        }
#    return config

def config_for_post():
    config = {
            "layers": [{
                "id": "default",
                "charset": "utf-8",
                "attributes": {
                    "id": "",
                    "code": "",
                    "name": ""
                }
            }]
        }
    return config

def create_svg_file(config, svgName, id):
    K = Kartograph()
    directory = os.path.join('static', 'img', str(id))
    if not os.path.exists(directory):
       os.makedirs(directory)
    tempName = os.path.splitext(svgName)[0]
    file_name = os.path.join(directory, tempName + ".svg")
    K.generate(config, outfile=file_name)


def shapefile_list(request):
    queryset = Shapefile.objects.all()
    context = {
        "object_list": queryset,
        }
    return render(request, "shapefile_list.html", context)

def svg_list(request):
    queryset = SvgFile.objects.all()
    context = {
        "object_list": queryset,
        }
    return render(request, "svg_list.html", context)

def svg_detail(request, id=None):
    instance = get_object_or_404(SvgFile, id=id)
    svgLayers = getLayersFroSvg(id)
    tempLayers = Layers.objects.all()
    print tempLayers
    layers = []
    for l in tempLayers:
        if l.idLayer in svgLayers:
            layers.append(l)
    context = {
        "layers": layers,
        "instance": instance        
        }
    return render(request, "svg_detail.html", context)

def maps_createsvg(request):
    queryset = SvgFile.objects.all()
    context = {
        "object_list": queryset,
        }
    
    if request.method == 'POST':
        list_of_input_ids=request.POST.getlist('choices')
        config = generate_config(list_of_input_ids)
        name = ""
        for i in list_of_input_ids:
            instance = get_object_or_404(SvgFile, id=i)
            name += instance.name

        save_svg(config, name)

    return render(request, "createsvg_list.html", context)

def generate_config(configArray):
    config = {
            "layers": []
        }
    
    for i in configArray:
        instance = get_object_or_404(SvgFile, id=i)
        tempstr = instance.config
        ItemInDict = dictFromString(tempstr)
        for item in ItemInDict:
            config['layers'].append(item)
 
    return config

def dictFromString(config):
    result = ast.literal_eval(config)
    return result 

def delete_svg(request, id=None):
    instance = get_object_or_404(SvgFile, id=id)
    finishSvg = instance.isOld
    instance.delete()

    messages.success(request, "smazano")

    if(finishSvg):
        return redirect("maps:svglist")
    else:
        return redirect("maps:svgfinallist")
    

def update_svg(request, id=None):
    instance = get_object_or_404(SvgFile, id=id)
    form = SvgForm(request.POST or None, instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "mapa se updatovala")
        return HttpResponseRedirect("maps:svgdetail")

    context = {
        "instance": instance,
        "form": form
        }
    return render(request, "svg_form.html", context)

def getAllWordsForSvg(filePath):
    words = []
    with open(os.path.join("static", filePath), 'r') as infile:
        svg = etree.parse( infile )
    
    SVG_NS = "{http://www.w3.org/2000/svg}"

    for element in svg.iter(SVG_NS + 'path'):
        word = element.get("data-name")
        if(word is None):
            continue
        
        words.append(word)
    return words

def addWordToPOFile(filePath):
    with open(os.path.join("static", filePath), 'r') as infile:
        svg = etree.parse( infile )

    pofile = polib.pofile('translation/pofiles.po', check_for_duplicates = True)

    SVG_NS = "{http://www.w3.org/2000/svg}"

    for element in svg.iter(SVG_NS + 'path'):
        word = element.get("data-name")
        if(word is None):
            continue

        entry = polib.POEntry(
            msgid = word,
        )

        try:
            pofile.append(entry)
        except:
            pass

        pofile.save('translation/pofiles.po')

def addWordsToSourceCSV(sourceWords, words):
    with open('translation/translations_cs.csv', 'a') as mycsvfile:
        writer = csv.writer(mycsvfile, delimiter=',', quotechar='"', quoting = csv.QUOTE_ALL)
        import itertools
        for sw,w in itertools.izip(sourceWords, words):
            writer.writerow([sw.encode('utf-8'), w.encode('utf-8')])

def transifexLogin():
    auth = ('zvolas8', 'marek888')
    return auth

#def transifexCreateNewProject(name):
#    source_language_code = 'cs-CZ'
#    repository_url = 'http://gmail.com'

#    url = 'http://transifex.com/api/2/projects/'
#    headers = {'content-type': 'application/json'}
#    data = {
#        'name': name, 'slug': name,
#        'source_language_code': source_language_code, 'description': name,
#        'private': 'False', 'repository_url': repository_url
#    }       
    
#    response = requests.post(
#        url, data=json.dumps(data), auth=transifexLogin(), headers=headers,
#    ) 

#    return response.status_code

def transifexCreateNewResource(resName, projectName):
    url = 'http://www.transifex.com/api/2/project/' + projectName + '/resources/'

    content = open('translation/translations_cs.csv', 'r').read()

    headers = {'content-type': 'application/json'}
    data = {
        'name': resName, 'slug': resName, 'content': content,
        'i18n_type': 'MAGENTO'
    }

    response = requests.post(
            url, data=json.dumps(data), auth=transifexLogin(), headers=headers,
    )
    return response.status_code

def transifexUpdateResource(resName, projectName):
    url = 'http://www.transifex.com/api/2/project/' + projectName + '/resource/' + resName + '/content/'
    content = open('translation/pofiles.po', 'r').read()

    headers = {'content-type': 'application/json'}
    data = {'content': content}

    response = requests.put(
            url, data=json.dumps(data), auth=transifexLogin(), headers=headers,
    )
    return response.status_code

def getFilepathBySvgId(id):
     instance = get_object_or_404(SvgFile, id=id)
     return instance.pathToFileSvg

def translation_word(request, id=None):
    #downloadAllTranslations()
    instance = get_object_or_404(SvgFile, id=id)
    sourceWords = getSourceStringForTranslate(getAllWordsForSvg(getFilepathBySvgId(id)))
    translateFiles = getAllTranslateFile()
    translateTitle = getTitleForFiles(translateFiles)
    words = getTranslate(sourceWords, translateFiles)

    context = { 
        "instance": instance,
        "words": words,
        "wordsTitle": translateTitle,
        }
    return render(request, "svg_words.html", context)

def getTitleForFiles(translateFiles):
    resultArray = []
    for file in translateFiles:
        regex = '^translations\_(?P<name>.*)\.csv$'
        m = re.match(regex, file)
        resultArray.append(m.group('name'))
    return resultArray

def getTranslate(sourceWord, translateFiles):
    resultArray = []

    for fileName in translateFiles:
        with open('translation/' + fileName, 'rb',) as mycsvfile:
            thedata = csv.reader(mycsvfile, dialect='mydialect')
            wordsArray = []
            for row in thedata:  
                if row[0].lower() in sourceWord:
                    wordsArray.append(row[1])

            resultArray.append(wordsArray)
    return resultArray

def getAllTranslateFile():
    resultArray = []
    for file in os.listdir("translation"):
        if file.endswith(".csv"):
            resultArray.append(file);
    return resultArray

def getSourceStringForTranslate(wordsArray):
    resultArray = []
    for word in wordsArray:
        resultArray.append(getSourceWordFromWord(word))

    return resultArray

def getSourceWordFromWord(word):
    return slugify(word, separator="_")

def svg_final_list(request):
    queryset = SvgFile.objects.all().filter(isOld=False)
    context = {
        "object_list": queryset,
        }
    return render(request, "svg_final_list.html", context)

def add_layer(request, id=None):
    form = ShapefileForm(request.POST or None, request.FILES or None)
    if request.method == "POST": 
        maps_create(request)

        newLayerId = SvgFile.objects.latest('id').id

        idList = []
        idList.append(newLayerId)
        idList.append(id)

        config = generate_config(idList)

        name = getNameForSvg(id)
        save_svg(config, name)
        
        setIsOldOnTrue(id)
        setIsOldOnTrue(newLayerId)
        
         
        return redirect("maps:svgfinallist")
   
    postConfig = json.dumps(config_for_post())
    layers = Layers.objects.all()

    context = {
        "layers": layers,
        "config": postConfig,
        "form": form
        }
    return render(request, "shapefile_form.html", context)


def delete_layer(request, id=None, layer=None):
    config = removeLayerFromConfig(getConfigAsDictById(id), layer)
    name = getNameForSvg(id)

    save_svg(config,name)
    setIsOldOnTrue(id)
    return redirect("maps:svgfinallist")

def removeLayerFromConfig(config, layer):
    resultConfig = {
            "layers": []
        }
    i = 0
    for l in config:
        if config[i]["id"] != layer:
            #del config[i]
            resultConfig['layers'].append(l)
            
        i+=1
    return resultConfig

def getLayersFroSvg(id):
    layers = []
    
    tempConfig = get_object_or_404(SvgFile, id=id).config
    config = dictFromString(tempConfig);
    for l in config:
        layers.append( l['id'])

    return layers

def remove_layer_list(request, id=None):
    layers = getLayersFroSvg(id)
    context = {
        "id": id,
        "layers": layers,
        }
    return render(request, "removeLayer.html", context)

def getConfigAsDictById(id):
    tempConfig = get_object_or_404(SvgFile, id=id).config
    config = dictFromString(tempConfig);
    return config

def getNameForSvg(id):
    return get_object_or_404(SvgFile, id=id).name

def setIsOldOnTrue(id):
    instance = get_object_or_404(SvgFile, id=id)
    instance.isOld = True
    instance.save()

def svgToFinalSvg(request, id=None):
    instance = get_object_or_404(SvgFile, id=id)
    instance.isOld = False;
    instance.save()
    return redirect("maps:svgfinallist")
    
def mapsSettings(request):
    context = {
        "id": id,
        }
    return render(request, "settings_base.html", context)
    
def SettingsLayer(request):
    layers = Layers.objects.all()
    context = {
        "layers": layers,
        }
    return render(request, "settings_layer.html", context)

def SettingsLayerEdit(request, id=None):
    instance = get_object_or_404(Layers, id=id)
    form = LayersForm(request.POST or None, instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #messages.success(request, "mapa se updatovala")
        return redirect("maps:settingsLayer")
    
    context = {
        "instance": instance,
        "form": form
        }
    return render(request, "settings_layer_edit.html", context)

def SettingsLayerAdd(request):
    form = LayersForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #messages.success(request, "mapa se updatovala")
        return redirect("maps:settingsLayer")
    
    context = {
        "form": form
        }
    return render(request, "settings_layer_add.html", context)

def Language(request):
    downloadAllTranslations()

    languageTag = getAllLanguage();
    language = []

    for l in languageTag:
        languageStats = getStatsForLanguage(l)
        languageStats['language'] = l
        language.append(languageStats)

    context = {
        "language": language
        }
    return render(request, "language.html", context)

def getAllLanguage():
    url = 'http://www.transifex.com/api/2/project/%s/resource/%s/' % (
            getProjectName(), getResourceName()
        )
    response = requests.get(url, auth=transifexLogin(), params={'details':''})

    content = json.loads(response.content)
    languages = [
        language['code'] for language in content['available_languages']
    ]

    return languages

def getStatsForLanguage(language):
    url = 'http://www.transifex.com/api/2/project/%s/resource/%s/stats/%s/' % (
            getProjectName(), getResourceName(), language
        )

    response = requests.get(url, auth=transifexLogin(), params={'details':''})

    content = json.loads(response.content)

    return content

def showCsv(request, name=None):
    with open('translation/translations_' + name + '.csv', 'rb',) as mycsvfile:
        thedata = csv.reader(mycsvfile, dialect='mydialect')
        wordsArray = []
        for row in thedata:
            wordsArray.append(row)  
     
    context = {
        "words": wordsArray
        }
    return render(request, "csv_view.html", context) 

def downloadAllTranslations():
    languages = getAllLanguage();
    
    for language in languages:
        url = 'http://www.transifex.com/api/2/project/%s/resource/%s/translation/%s/' % (
           getProjectName(), getResourceName(), language
        )
        query = {
            #'file': ''
        }
        
        response = requests.get(url, auth=transifexLogin(), params=query)
        data = json.loads(response.text)
        #print data['content']
        textRow = data['content']
        textRow  = textRow.encode("utf-8").split()

        handle = codecs.open('translation/translations_' + language + '.csv', 'w', "utf-8")
        for line in textRow:
            handle.write(line.decode('utf-8'))
            handle.write("\r\n")
        handle.close()

def configList(request):
    configs = Config.objects.all()
    context = {
        "configs": configs
        }
    return render(request, "config_list.html", context)

def configAdd(request):

    if request.method == 'POST':
        config = request.POST['myConfig']
        name = request.POST['configName']
        
        configObject = Config()
        configObject.name = name
        configString = dictFromString(config)
        
        configDict = {
            "layers": []
        }
        
        configDict['layers'].append(configString)

        #kontrola ID vrstvy
        valid = False
        layers = Layers.objects.all()
        for layer in layers:
             if configDict['layers'][0]['id'] == layer.idLayer:
                 valid = True

        configObject.valid = valid
        #configObject.config = configDict['layers']
        configObject.config = json.dumps(configDict)
        configObject.save()

    context = {
        
        }
    return render(request, "config_add.html", context)

def createShapefileFromConfig(request):

    if request.method == 'POST':
        configId = request.POST['shpConfig']
        configObj = get_object_or_404(Config, id=configId)
        tempConfig = dictFromString(configObj.config)
        layer = tempConfig['layers'][0]['id']
        layerObj = get_object_or_404(Layers, idLayer=layer)

        shpObject = Shapefile()
        shpName = request.POST['shpName']
        shpObject.name = shpName
        shpObject.layerName = layerObj
        
        for f in request.FILES.getlist('files'):
            if f.name[-3:] == "shp":
                shpObject.shapefileName = f.name
                shpObject.fileshp = f
                tempfile = f 

        shpObject.save()
            
        instance = get_object_or_404(Shapefile, id=shpObject.id)
        instance.fileshp = tempfile
        instance.save()

        for f in request.FILES.getlist('files'):
            if f.name[-3:] != "shp":
                path = default_storage.save(os.path.join(settings.MEDIA_ROOT, str(instance.id), f.name), ContentFile(f.read()))

        config = addSrcToConfigDict(tempConfig, instance.id, tempfile.name)
        svgId = save_svg(config, shpName)
        svgWords = getAllWordsForSvg(getFilepathBySvgId(svgId))
        sourceWords = getSourceStringForTranslate(svgWords)
        addWordsToSourceCSV(sourceWords, svgWords)
        
        resName = getResourceName()
        projectName = getProjectName()

        re = transifexCreateNewResource(resName, projectName)
        print re


        deleteFolder = os.path.join(settings.MEDIA_ROOT, "None") 
        shutil.rmtree(deleteFolder)

        messages.success(request, "shapefile byl ulozen")

    configs = Config.objects.all().filter(valid=True)
    context = {
        "configs": configs
        }
    return render(request, "shapefile_from_config.html", context)

def configEdit(request, id=None):
    instance = get_object_or_404(Config, id=id)
    
    if request.method == 'POST':
        instance.name = request.POST['configName']
        
        config = request.POST['myConfig']
        configString = dictFromString(config)

        #kontrola ID vrstvy
        valid = False
        layers = Layers.objects.all()
        for layer in layers:
             if configString['layers'][0]['id'] == layer.idLayer:
                 valid = True

        instance.valid = valid

        instance.config = json.dumps(configString)
        instance.save()
    
    context = {
        "instance": instance,
        }
    return render(request, "config_edit.html", context)

def addLayerFromConfig(request, id=None):

    if request.method == "POST": 
        createShapefileFromConfig(request)

        newLayerId = SvgFile.objects.latest('id').id

        idList = []
        idList.append(newLayerId)
        idList.append(id)

        config = generate_config(idList)

        name = getNameForSvg(id)
        save_svg(config, name)
        
        setIsOldOnTrue(id)
        setIsOldOnTrue(newLayerId)
        
         
        return redirect("maps:svgfinallist")

    configs = Config.objects.all().filter(valid=True)
    context = {
        "configs": configs
        }
    return render(request, "shapefile_from_config.html", context)
