import os
import shutil
import re
import ast
import polib
import requests
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from kartograph import Kartograph

from lxml import etree

# Create your views here.

from .forms import ShapefileForm, SvgForm
from .models import Shapefile, SvgFile




def maps_create(request):
    form = ShapefileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        file = form.save(commit=False)
        shpName = form.cleaned_data['name']
        layerName = form.cleaned_data['layerName']
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
                path = default_storage.save((str(instance.id) + "\\" + f.name), ContentFile(f.read()))
        
        projectName = 'slepemapy'
        resName = 'czwords'

        isFileExist = os.path.exists("translation/pofiles.po")
        if(isFileExist == False):
            createPOFile()
            pr = transifexCreateNewProject(projectName)
            print pr
            re = transifexCreateNewResource(resName, projectName)
            print re
        
        config = create_config(instance.id, tempfile.name, layerName)
        pathPO = save_svg(config, shpName)
        addWordToPOFile(pathPO)
        transifexUpdateResource(resName, projectName)

        deleteFolder = "C:\\Users\marek\Documents\pythonprojekt\slepeMapy\media_cdn\\None" #najit slozku automaticky TODO
        shutil.rmtree(deleteFolder)

        messages.success(request, "shapefile byl ulozen")
        #return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form
        }
    return render(request, "shapefile_form.html", context)

def save_svg(config, name):
    svg = SvgFile()
    tName =  os.path.splitext(name)[0]
    tConfig = create_config_format(config)
    svg.name = name
    svg.config = tConfig
    svg.save()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = "img\\" + str(svg.id) + "\\" + tName + ".svg"
    svg.pathToFileSvg = path
    svg.save()
    create_svg_file(config, name, svg.id)
    return path

def create_config_format(config):
    c = config['layers']
    return c

def create_config(id, FILE_NAME, layerName):

    config = {
            "layers": [{
                "id": str(layerName),
                "src": str("C:\\Users\marek\Documents\pythonprojekt\slepeMapy\media_cdn\\" + str(id) + "\\" + FILE_NAME),
                "attributes": {
                    "id": "iso_a2",
                    "code": "name",  
                    "name": "name"
                }
            }]
        }
    return config

def create_svg_file(config, svgName, id):
    K = Kartograph()
    directory = 'static\img\\' + str(id)
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
    context = {
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
    instance.delete()
    messages.success(request, "smazano")
    return redirect("maps:svglist")

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

def addWordToPOFile(filePath):
    with open("static\\" + filePath, 'r') as infile: 
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

def createPOFile():
    po = polib.POFile()
    po.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': 'you@example.com',
        'POT-Creation-Date': '2007-10-18 14:00+0100',
        'PO-Revision-Date': '2007-10-18 14:00+0100',
        'Last-Translator': 'Automatically generated',
        'Language-Team': 'none',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
    }

    #'Language': 'cs_CZ',
    #'Plural-Forms': 'nplurals=3; plural=(n==1) ? 0 : (n>=2 && n<=4) ? 1 : 2;',

    entry = polib.POEntry(
        msgid = "prvni slovo",
    )

    po.append(entry)

    os.mkdir("translation")  
    po.save('translation/pofiles.po')

def transifexLogin():
    auth = ('bworktest', 'bworktest1245')
    return auth

def transifexCreateNewProject(name):
    source_language_code = 'cs-CZ'
    repository_url = 'http://gmail.com'

    url = 'http://transifex.com/api/2/projects/'
    headers = {'content-type': 'application/json'}
    data = {
        'name': name, 'slug': name,
        'source_language_code': source_language_code, 'description': name,
        'private': 'False', 'repository_url': repository_url
    }       
    
    response = requests.post(
        url, data=json.dumps(data), auth=transifexLogin(), headers=headers,
    ) 

    return response.status_code

def transifexCreateNewResource(resName, projectName):
    url = 'http://www.transifex.com/api/2/project/' + projectName + '/resources/'
    print url

    content = open('translation/pofiles.po', 'r').read()

    headers = {'content-type': 'application/json'}
    data = {
        'name': resName, 'slug': resName, 'content': content,
        'i18n_type': 'PO'
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
    

def translation_word(reques, id=None):
    instance = get_object_or_404(SvgFile, id=id)
    svg = etree.parse(open("static\\img\\38\\hory.svg", 'r'))
    
    SVG_NS = "http://www.w3.org/2000/svg"

    for node in svg.findall('.//{%s}path' % SVG_NS):
        print 'n=', node
        for n in node.findall('.//{%s}data-name' % SVG_NS):
            print n

    
    