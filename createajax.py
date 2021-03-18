import string
import random
import fileinput
import re
import os
import sys
import shutil
import fileinput
import pathlib

lookup = 'hiersollajaxrein'
Appname = input("In welcher App sollen die models erstellt werden: ")
Pagename = input("Seitennamen wo Ajax hinzugefügt werden soll: ")
urlname = input("Ajax-url-Name: ")
login_required = input("Ist für View eine Login erforderlich ja/nein: ")
anzahlFormsForBackend = input("Anzahl der übergebenen Forms ans Backend: ")
anzahlFormsForBackend = int(anzahlFormsForBackend)
anzahlFormsForBackend = range(anzahlFormsForBackend)


FormList = []

for i in anzahlFormsForBackend:
    counter = anzahlFormsForBackend[i]
    FormNumber = str(counter)
    Form = input("Form "+FormNumber+": ")
    FormList.append(Form)

RueckgabeDatenArt = input("Soll die Rückgabe der Daten ans Frontend als text oder als json zurückkommen: ")

CurrentPath = pathlib.Path(__file__).parent.absolute()
CurrentPath = str(CurrentPath)+"/"+Appname
FilepathHTMLPage = CurrentPath+'/templates/'+Pagename+'.html'
FilepathAppforms = CurrentPath+'/CustomForms/appforms.py'
FilepathAppUrls = CurrentPath+'/urls.py'
FilepathAppViews = CurrentPath+'/views.py'




#Findet in der HTML-Page die Zeile in der das AjaxScript eingesetzt werden soll
x=0
with open(FilepathHTMLPage) as myFile:
    for num, line in enumerate(myFile, 1):
        if lookup in line:
            x = num

################################################################################
# Setzt das AjaxScript an die gewünschte Stellen mit wunschUrl und Forms ein
################################################################################
def modify_file(file_name, pattern, value=""):
    fh = fileinput.input(file_name, inplace=True)
    for line in fh:
        replacement = value
        line = re.sub(pattern, replacement, line)
        sys.stdout.write(line)
    fh.close()


# Generiert einen RandomKey für die AjaxFormen, das diese an die richtige Stelle in der Html-Page eingesetzt werden
letters = string.ascii_lowercase
RandomKeyForAjax = '###RandomKey:'+(''.join(random.choice(letters) for i in range(10)))


PositionFromAjaxInsert = x-1
a_file = open(FilepathHTMLPage, "r")
list_of_lines = a_file.readlines()
list_of_lines[PositionFromAjaxInsert] = "\t$.ajax({\n\t\ttype: 'POST',\n\t\turl: '"+urlname + \
    "/',\n\t\tdata: {\n\t\t\tcsrfmiddlewaretoken: '{{ csrf_token }}',\n\t\t\t//PlaceForForms"+RandomKeyForAjax+"\n\t\t}, \n\t\tdataType: 'text', \n\t\tsuccess: function(data) {\n\n\t\t}, error: function() {\n\t\t\tconsole.log('Fehler in AjaxPost. Url: /" +urlname+"/'); \n\t\t}\n\t})\n"

a_file = open(FilepathHTMLPage, "w")
a_file.writelines(list_of_lines)
a_file.close()

counter = 0
for i in FormList:
    counter += 1
    counterString = str(counter)  
    modify_file(FilepathHTMLPage, "//PlaceForForms"+RandomKeyForAjax, i+": Javascriptvariable"+counterString+",\n\t\t\t//PlaceForForms"+RandomKeyForAjax)


################################################################################
# Generiert die Appforms in appforms.py für diesen AjaxPost
################################################################################

if len(FormList) > 0:
    appforms = open(FilepathAppforms, "a")
    appforms.write(
        "\n\nclass "+urlname+"Form(forms.Form):\n\n\t#placeForAnotherForms"+RandomKeyForAjax)
    appforms.close()

    for i in FormList:
        modify_file(FilepathAppforms, "#placeForAnotherForms"+RandomKeyForAjax, i+" = forms.CharField(\n\t\twidget=appwidgets.myTextWidget(),\n\t\tlocalize=True,\n\t\trequired=False,\n\t)\n\n\t#placeForAnotherForms"+RandomKeyForAjax)


################################################################################
# Generiert die urls in urls.py für diesen AjaxPost
################################################################################
modify_file(FilepathAppUrls,
            "urlpatterns = \\[", "urlpatterns = [\n\tpath('"+urlname+"/', views."+urlname+", name='"+urlname+"'),")


################################################################################
# Generiert die views in views.py für diesen AjaxPost
################################################################################

if login_required == "ja":
    login_required = "@login_required"
else:
    login_required = ""

addviews = open(FilepathAppViews, "a")
addviews.write(
    "\n\n"+login_required+"\ndef "+urlname+"(request):\n\tif request.method == 'POST':\n\t\t###WaitforForms###"+RandomKeyForAjax)
addviews.close()

if len(FormList) > 0:
    modify_file(FilepathAppViews, "###WaitforForms###"+RandomKeyForAjax, "form = "+Appname+"forms."+ urlname +
                "Form(request.POST)\n\t\tif form.is_valid():\n\t\t\t###WaitforForms###"+RandomKeyForAjax)
    for i in FormList:
        modify_file(FilepathAppViews, "###WaitforForms###"+RandomKeyForAjax, i +
                    " = form.cleaned_data['"+i+"']\n\t\t\t###WaitforForms###"+RandomKeyForAjax)
    
    if RueckgabeDatenArt == "text":
        modify_file(FilepathAppViews, "###WaitforForms###"+RandomKeyForAjax,
                    "\n\t\t\tx=1\n\treturn HttpResponse(x, content_type='text/html')")

    if RueckgabeDatenArt == "json":
        modify_file(FilepathAppViews, "###WaitforForms###"+RandomKeyForAjax,
                    "\n\t\t\tBackToFrontendlist=list(mylist)\n\t\t\tBackToFrontendlist=json.dumps(BackToFrontendlist, ensure_ascii=False).encode('utf8')\n\n\treturn HttpResponse(BackToFrontendlist, content_type='application/json')")


else:

    if RueckgabeDatenArt == "text":
        modify_file(FilepathAppViews, "###WaitforForms###"+RandomKeyForAjax,
                    "x=1\n\treturn HttpResponse(x, content_type='text/html')")

    if RueckgabeDatenArt == "json":
        modify_file(FilepathAppViews, "###WaitforForms###"+RandomKeyForAjax,
                    "\n\t\tBackToFrontendlist=list(mylist)\n\t\tBackToFrontendlist=json.dumps(BackToFrontendlist, ensure_ascii=False).encode('utf8')\n\n\treturn HttpResponse(BackToFrontendlist, content_type='application/json')")


print("Ajax erfolgreich angelegt!")
