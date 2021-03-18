import fileinput
import re
import os
import sys
import shutil
import fileinput
import pathlib
CurrentPath = pathlib.Path(__file__).parent.absolute()

Appname = input("In welcher App soll die Seite erstellt werden: ")
Pagename = input("Wie soll die Seite heißen: ")

# templatepath = CurrentPath+'/'+Appname+'/templates'
CurrentPath = str(CurrentPath)

shutil.copyfile('/Users/florianbuchfink/Desktop/Entwicklung/Entwicklung/DjangoWorkflow/startseite.html', CurrentPath+'/'+Appname+'/templates/'+Pagename+'.html')

with fileinput.FileInput(CurrentPath+'/'+Appname+'/templates/'+Pagename+'.html', inplace=True) as file:
    for line in file:
        print(line.replace("Startseite", Pagename), end='')


def modify_file(file_name, pattern, value=""):
    fh = fileinput.input(file_name, inplace=True)
    for line in fh:
        replacement = value
        line = re.sub(pattern, replacement, line)
        sys.stdout.write(line)
    fh.close()


modify_file(CurrentPath+'/'+Appname+'/urls.py',
            "urlpatterns = \\[", "urlpatterns = [\n\tpath('"+Pagename+"', views."+Pagename+", name='"+Pagename+"'),")


addviews = open(CurrentPath+'/'+Appname+"/views.py", "a")
addviews.write(
    "\n\n\ndef "+Pagename+"(request): \n\treturn render(request, '"+Pagename+".html')")
addviews.close()

with fileinput.FileInput(CurrentPath+'/'+Appname+'/templates/'+Pagename+'.html', inplace=True) as file:
    for line in file:
        print(line.replace("xxxstaticappnamexxx", Appname), end='')


