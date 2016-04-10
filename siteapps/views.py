from django.shortcuts import render
import cloudconvert
from .models import Document, Organization, InmergenceUser
import uuid
import os
import zipfile
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UserForm, UserProfileForm
#We added this to handle the HttpResponse in this particular manner.
from django.http.response import HttpResponse
from html.parser import HTMLParser
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def clean_html(path, org_name, doc_name):
    s = '\\'
    # path to zip file
    pz = path + org_name + s + doc_name
    # path to location zip files are loaded to
    pt = path + org_name + s
    fh = open(pz, 'rb')
    z = zipfile.ZipFile(fh)
    for name in z.namelist():
        outpath = pt
        z.extract(name, outpath)
    fh.close()

    import os, shutil
    folder = pt
    for the_file in os.listdir(folder):
        if str(the_file)[-4:] == "html":
            pass
        else:
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    with open(pz.replace('zip', 'html'), 'r+', encoding="utf8") as html:
        with open(pz[:-4] + '-rendered.html', 'a', encoding="utf8") as wrt:
            wrt.write('{% extends "base.html" %}\n')
            wrt.write('{% block content %}\n')
            for line in html.readlines()[37:-2]:
                wrt.write(line)
            wrt.write('{% endblock %}\n')


def index(request):
    m = BASE_DIR + "\\media\\"
    t = BASE_DIR + "\\templates\\"
    if request.method == "POST":
        usr = InmergenceUser.objects.get(user=request.user)
        org = Organization.objects.get(user=usr)
        fformat = request.POST['fileFormat']
        file = request.FILES['file']
        id = uuid.uuid4()
        doc, created = Document.objects.get_or_create(
            id=id,
            organization=org,
            name=file.name,
            file=file,
            html_name=file.name[:-3]+'html'
        )
        doc.save()
        api = cloudconvert.Api('HKi3ooM6JI_caLFxb90B5lYONnKmoGjGNZ8R3Ozx22XB9pJJDzk1wx9fBgJEDqu-s_gmwWc1R31h_YPABQOZjw')
        process = api.convert({
            "input": "upload",
            "email": "false",
            "inputformat": fformat,
            "outputformat": "html",
            "preset": "ytfLaX3GgM",
            "file": open(m + str(doc.file), 'rb')
        })

        path = t + org.name.replace(' ', '_') + '\\'
        if not os.path.exists(path):
            os.mkdir(path)
        process.wait()
        process.download(path)
        real_file_name_to_zip = str(doc.file).replace(str(org.name).replace(" ", "_") + "/", "").replace('pdf', 'zip')
        clean_html(t, str(org.name).replace(' ', '_'), real_file_name_to_zip)
        context = {}
        return render(request, 'index.html', context)
    else:
        context = {}
        return render(request, 'index.html', context)


def org(request, org):
    org = org.replace('_', ' ')
    cur_org = Organization.objects.get(name=org)
    docs = Document.objects.filter(organization=cur_org)
    return render(request, 'org.html', {'org': cur_org, 'doc': docs})


def doc(request, org, docu):
    print(org)
    print(docu)
    org_no_under = org.replace('_', ' ')
    cur_org = Organization.objects.get(name=org_no_under)
    doc = Document.objects.get(id=docu)
    loca = str(doc.file)[:-3] + 'html'
    print(loca)
    return render(request, str(doc.file)[:-4] + '-rendered.html', {})


# Create your views here.

def display_markup(request):
    return render(request, 'siteapps/markup.html')


def display_readings(request):
    return render(request, 'siteapps/readings.html')


def register(request):
    pass
#     if request.method == 'POST':
#         uf = UserForm(request.POST, prefix='user')
#         upf = UserProfileForm(request.POST, prefix='userprofile')
#         if uf.is_valid() * upf.is_valid():
#             user = uf.save()
#             userprofile = upf.save(commit=False)
#             userprofile.user = user
#             userprofile.save()
#             return HttpResponseRedirect('/')
#     else:
#         uf = UserForm(prefix='user')
#         upf = UserProfileForm(prefix='userprofile')
#     return django.shortcuts.render_to_response('register.html',
#                                                dict(userform=uf,
#                                                     userprofileform=upf),
#                                                context_instance=django.template.RequestContext(request))
#     return render(request, "register.html", {'form': form})
