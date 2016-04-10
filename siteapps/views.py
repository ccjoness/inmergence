from django.shortcuts import render
import cloudconvert
from .models import Document, Organization, InmergenceUser
import uuid
import os
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UserForm, UserProfileForm
#We added this to handle the HttpResponse in this particular manner.
from django.http.response import HttpResponse


def clean_html(path, doc_name):
    doc_name = str(doc_name).replace('/', '\\')
    print(path + doc_name[:-3] + 'txt')
    f = open(path + doc_name[:-3] + 'txt', 'r+', encoding='utf8')
    x = open(path + doc_name[:-3] + 'html', 'w', encoding='utf8')

    header1 = "{% extends 'base.html' %}\n"
    header2 = "{% block content %}\n"
    footer1 = "\n{% endblock %}"
    x.write(header1)
    x.write(header2)
    for line in f.readlines():
        x.write(line)
    x.write(footer1)


def index(request):
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
            "outputformat": "txt",
            "preset": "ytfLaX3GgM",
            "file": open('C:\\projects\\inmergence_app\\media\\' + str(doc.file), 'rb')
        })

        path = 'C:\\projects\\inmergence_app\\templates\\' + org.name.replace(' ', '_') + '\\'
        if not os.path.exists(path):
            os.mkdir(path)
        process.wait()
        process.download(path)
        clean_html('C:\\projects\\inmergence_app\\templates\\', doc.file)
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
    return render(request, str(doc.file)[:-3] + 'html', {})


# Create your views here.

def display_markup(request):
    return render(request, 'siteapps/markup.html')

def display_readings(request):
    return render(request, 'siteapps/readings.html')


def display_registration(request):
    return render(request, 'siteapps/registration.html')

#
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
