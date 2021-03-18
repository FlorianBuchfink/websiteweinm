from django.shortcuts import render

# Create your views here.

from website import models as modwebsite
#from website.helpers.modelHelper import ModelHelper as modhelper
from django.http import HttpResponse
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from website.CustomForms import appforms as websiteforms
from django.contrib.auth.models import User
import json


def index(request):
	return render(request, 'startseite.html')