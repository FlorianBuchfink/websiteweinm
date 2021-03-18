import fileinput
import re
import os
import sys
import shutil
import fileinput
import pathlib
import string
import random
CurrentPath = pathlib.Path(__file__).parent.absolute()

Appname = input("In welcher App sollen die models erstellt werden: ")
Modelname = input("Wie soll das model heißen: ")
anzahlModelsForBackend = input("Anzahl der zu schreibenen Models: ")
anzahlModelsForBackend = int(anzahlModelsForBackend)
anzahlModelsForBackend = range(anzahlModelsForBackend)

# Erfasst alle Models (Namen) welche erstellt werden sollen
ModelList = []
for i in anzahlModelsForBackend:
    counter = anzahlModelsForBackend[i]
    ModelNumber = str(counter)
    Model = input(Modelname+" Model "+ModelNumber+": ")
    ModelList.append(Model)

CurrentPath = str(CurrentPath)
modelpath = CurrentPath+'/'+Appname+'/'


def modify_file(file_name, pattern, value=""):
    fh = fileinput.input(file_name, inplace=True)
    for line in fh:
        replacement = value
        line = re.sub(pattern, replacement, line)
        sys.stdout.write(line)
    fh.close()


# Generiert einen RandomKey für die Modles, das diese an die richtige Stelle in der models.py eingesetzt werden
letters = string.ascii_lowercase
RandomKeyForModels = '###RandomKey:' + \
    (''.join(random.choice(letters) for i in range(10)))



addmodels = open(CurrentPath+'/'+Appname+"/models.py", "a")
addmodels.write(
    "\n\n\nclass "+Modelname+"(models.Model): \n\t"+RandomKeyForModels)
addmodels.close()

# Erfasst von den zuvor erstellten Models die Details z.b. CharField() oder DateTimeField(), ForeignKey, DecimalField
for i in ModelList:
    ModelArt = input("Was für eine Art ist Modeleintrag: "+i+" ForeignKey=1, CharField=2, DecimalField=3, DateTimeField=4: ")
    if ModelArt == "1":
        modelForeignKey = input("Von welchem Model ist dieser Eintrag ForeignKey: ")
        modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, i+" = models.ForeignKey("+modelForeignKey+", on_delete=models.CASCADE, related_name='"+i+"_fromModel_"+Modelname+"_getData_fromModel_"+modelForeignKey+"')\n\t"+RandomKeyForModels)
    if ModelArt == "2":
        modelCharLength = input("Wieviel Zeichen wird dieses Feld maximal haben: ")
        modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, i+" = models.CharField(max_length="+modelCharLength+", blank=True)\n\t"+RandomKeyForModels)
    if ModelArt == "3":
        modelDecimalPlaces = input("Wieviel Kommastellen wird die Zahl maximal haben: ")
        modelDigitsLength = input("Wie lang inkl. Kommastellen wird die Zahl maximal sein: ")
        modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, i+" = models.DecimalField(max_digits="+modelDigitsLength+", decimal_places="+modelDecimalPlaces+", default=0)\n\t"+RandomKeyForModels)
    if ModelArt == "4":
        modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, i+" = models.DateTimeField()\n\t"+RandomKeyForModels)


returnStringSignList = []
for i in ModelList:
    returnStringSignList.append("%s")

returnStringSign = " ".join(returnStringSignList)


modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, "\n\tdef __str__(self):\n\t\t"+RandomKeyForModels)
modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, "return '"+returnStringSign+"' % (\n\t\t\t"+RandomKeyForModels)
for i in ModelList:
   modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, "self."+i+",\n\t\t\t"+RandomKeyForModels) 

modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, "\n\t\t)\n\t"+RandomKeyForModels) 


modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, "\n\tdef __unicode__(self):\n\t\t"+RandomKeyForModels)
modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, "return '"+returnStringSign+"' % (\n\t\t\t"+RandomKeyForModels)
for i in ModelList:
   modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, "self."+i+",\n\t\t\t"+RandomKeyForModels) 

modify_file(CurrentPath+'/'+Appname+"/models.py", RandomKeyForModels, "\n\t\t)\n\t"+RandomKeyForModels) 


#########################################################################
# Erstellt die modelHelpers 
#########################################################################

modelHelperParameter = []
for i in ModelList:
    parameter = Modelname+"_"+i
    modelHelperParameter.append(parameter)

modelHelperParameterString = ", ".join(modelHelperParameter)

addmodelHelper = open(CurrentPath+'/'+Appname+"/helpers/modelHelper.py", "a")
addmodelHelper.write(
    "\n\n\tdef create_"+Modelname+"("+modelHelperParameterString+"): \n\n\t\t"+RandomKeyForModels)
addmodelHelper.close()
modify_file(CurrentPath+'/'+Appname+"/helpers/modelHelper.py", RandomKeyForModels, Modelname+"_modelhelper = models."+Modelname+"()\n\t\t"+RandomKeyForModels)

counter = 0
for i in ModelList:
    modify_file(CurrentPath+'/'+Appname+"/helpers/modelHelper.py", RandomKeyForModels,
                Modelname+"_modelhelper."+i+" = "+modelHelperParameter[counter]+"\n\t\t"+RandomKeyForModels)
    counter += 1

modify_file(CurrentPath+'/'+Appname+"/helpers/modelHelper.py", RandomKeyForModels,
            "\n\t\treturn "+Modelname+"_modelhelper\n")


print("Model <"+Modelname+"> inkl. modelHelper <create_"+Modelname+"> erfolgreich angelegt!")
