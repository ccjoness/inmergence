from django.shortcuts import render
import cloudconvert
from .models import Document, Organization, InmergenceUser
import uuid
import os
import zipfile
import re
from .forms import UserForm, UserProfileForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def inplace_change(filename, old_string, new_string):
    s = open(filename, encoding="utf8").read()
    if old_string in s:
        print('Changing "{old_string}" to "{new_string}"'.format(**locals()))
        s = s.replace(old_string, new_string)
        f = open(filename, 'w', encoding="utf8")
        f.write(s)
        f.flush()
        f.close()
    else:
        print('No occurrences of "{old_string}" found.'.format(**locals()))


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

    with open(pz.replace('.zip', '.html'), 'r+', encoding="utf8") as html:
        with open(pz[:-4] + '-rendered.html', 'a', encoding="utf8") as wrt:
            wrt.write('{% extends "base.html" %}\n')
            wrt.write('{% block content %}\n')
            for line in html.readlines()[37:-2]:
                wrt.write(line)
            wrt.write('{% endblock %}\n')

    html_escape_table = [
        ['&#32;', ' '],
        ['&#33;', '!'],
        ['&#34;', '"'],
        ['&#35;', '#'],
        ['&#36;', '$'],
        ['&#37;', '%'],
        ['&#38;', '&'],
        ['&#39;', '\''],
        ['&#40;', '('],
        ['&#41;', ')'],
        ['&#42;', '*'],
        ['&#43;', '+'],
        ['&#44;', ','],
        ['&#45;', '-'],
        ['&#46;', '.'],
        ['&#47;', '/'],
        ['&#48;', '0'],
        ['&#57;', '9'],
        ['&#58;', ':'],
        ['&#59;', ';'],
        ['&#60;', '<'],
        ['&#61;', '='],
        ['&#62;', '>'],
        ['&#63;', '?'],
        ['&#64;', '@'],
        ['&#65;', 'A'],
        ['&#90;', 'Z'],
        ['&#91;', '['],
        ['&#92;', '\\'],
        ['&#93;', ']'],
        ['&#94;', '^'],
        ['&#95;', '_'],
        ['&#96;', '`'],
        ['&#97;', 'a'],
        ['&#122;', 'z'],
        ['&#123;', '{'],
        ['&#124;', '|'],
        ['&#125;', '}'],
        ['&#126;', '~'],
        ['&#160;', ' '],
        ['&#161;', '¡'],
        ['&#162;', '¢'],
        ['&#163;', '£'],
        ['&#164;', '¤'],
        ['&#165;', '¥'],
        ['&#166;', '¦'],
        ['&#167;', '§'],
        ['&#168;', '¨'],
        ['&#169;', '©'],
        ['&#170;', 'ª'],
        ['&#171;', '«'],
        ['&#172;', '¬'],
        ['&#173;', '­'],
        ['&#174;', '®'],
        ['&#175;', '¯'],
        ['&#176;', '°'],
        ['&#177;', '±'],
        ['&#178;', '²'],
        ['&#179;', '³'],
        ['&#180;', '´'],
        ['&#181;', 'µ'],
        ['&#182;', '¶'],
        ['&#183;', '·'],
        ['&#184;', '¸'],
        ['&#185;', '¹'],
        ['&#186;', 'º'],
        ['&#187;', '»'],
        ['&#188;', '¼'],
        ['&#189;', '½'],
        ['&#190;', '¾'],
        ['&#191;', '¿'],
        ['&#192;', 'À'],
        ['&#193;', 'Á'],
        ['&#194;', 'Â'],
        ['&#195;', 'Ã'],
        ['&#196;', 'Ä'],
        ['&#197;', 'Å'],
        ['&#198;', 'Æ'],
        ['&#199;', 'Ç'],
        ['&#200;', 'È'],
        ['&#201;', 'É'],
        ['&#202;', 'Ê'],
        ['&#203;', 'Ë'],
        ['&#204;', 'Ì'],
        ['&#205;', 'Í'],
        ['&#206;', 'Î'],
        ['&#207;', 'Ï'],
        ['&#208;', 'Ð'],
        ['&#209;', 'Ñ'],
        ['&#210;', 'Ò'],
        ['&#211;', 'Ó'],
        ['&#212;', 'Ô'],
        ['&#213;', 'Õ'],
        ['&#214;', 'Ö'],
        ['&#215;', '×'],
        ['&#216;', 'Ø'],
        ['&#217;', 'Ù'],
        ['&#218;', 'Ú'],
        ['&#219;', 'Û'],
        ['&#220;', 'Ü'],
        ['&#221;', 'Ý'],
        ['&#222;', 'Þ'],
        ['&#223;', 'ß'],
        ['&#224;', 'à'],
        ['&#225;', 'á'],
        ['&#226;', 'â'],
        ['&#227;', 'ã'],
        ['&#228;', 'ä'],
        ['&#229;', 'å'],
        ['&#230;', 'æ'],
        ['&#231;', 'ç'],
        ['&#232;', 'è'],
        ['&#233;', 'é'],
        ['&#234;', 'ê'],
        ['&#235;', 'ë'],
        ['&#236;', 'ì'],
        ['&#237;', 'í'],
        ['&#238;', 'î'],
        ['&#239;', 'ï'],
        ['&#240;', 'ð'],
        ['&#241;', 'ñ'],
        ['&#242;', 'ò'],
        ['&#243;', 'ó'],
        ['&#244;', 'ô'],
        ['&#245;', 'õ'],
        ['&#246;', 'ö'],
        ['&#247;', '÷'],
        ['&#248;', 'ø'],
        ['&#249;', 'ù'],
        ['&#250;', 'ú'],
        ['&#251;', 'û'],
        ['&#252;', 'ü'],
        ['&#253;', 'ý'],
        ['&#254;', 'þ'],
        ['&#255;', 'ÿ']
    ]

    for x in html_escape_table:
        inplace_change(pz[:-4] + '-rendered.html', x[0], x[1])


def upload_document(request):
    m = BASE_DIR + "\\media\\"
    t = BASE_DIR + "\\templates\\"
    context = {}
    if request.method == "POST":
        usr = User.objects.get(username=request.user)
        in_user = InmergenceUser.objects.get(user=usr)
        org = Organization.objects.get(user=usr)
        fformat = request.POST['fileFormat']
        file = request.FILES['file']
        id = uuid.uuid4()
        doc, created = Document.objects.get_or_create(
            id=id,
            organization=org,
            name=file.name,
            file=file,
            html_name=file.name[:-3] + 'html',
            user=in_user
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
        real_file_name_to_zip = str(doc.file).replace(str(org.name).replace(" ", "_") + "/", "").replace('.pdf', '.zip')
        clean_html(t, str(org.name).replace(' ', '_'), real_file_name_to_zip)
        context = {}

    return render(request, 'index.html', context)


def index(request):
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


@login_required
def dashboard(request):

    usr = User.objects.get(username=request.user)
    org = Organization.objects.get(user=usr)
    user_docs = Document.objects.filter(user__user=usr)
    org_html_name = org.name.replace(' ', '_')
    print(org_html_name)
    return render(request, 'dashboard.html', {'org': org,
                                              'user_docs': user_docs,
                                              'org_html': org_html_name
                                              })


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'registration/login.html', {})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
