from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.

from xxxwebsite2 import models as modwebsite
#from website.helpers.modelHelper import ModelHelper as modhelper
from django.http import HttpResponse
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from xxxwebsite2.CustomForms import appforms as websiteforms
from django.contrib.auth.models import User
import json


def index(request):
	return render(request, 'startseite1.html')


def sendkontaktformular(request):
	if request.method == 'POST':
		form = websiteforms.sendkontaktformularForm(request.POST)
		if form.is_valid():
			vorname = form.cleaned_data['vorname']
			nachname = form.cleaned_data['nachname']
			email = form.cleaned_data['email']
			telefon = form.cleaned_data['telefon']
			nachricht = form.cleaned_data['nachricht']
			subject = "Anfrage"
			subject, from_email, to = subject, 'anfrage@buchfinkmailservice.de', 'florian@buchfink.de'
			text_content = ''
			html_content = '<span>'+'Eine neue Anfrage über Ihre Website'+' '+'</br>'+'</br>'+'<div class="div" style="background: #4c4c4ce3; height: 30px; width: 100%"> </div>'+'</br>' + '<strong>Kontaktdaten:</strong>'+' '+'</br>'+vorname + ' ' + nachname + " " + '</br>Telefon: ' + telefon + '</br>Email: '+email + '</br>' + '</br>' +\
                            '<div class="div" style="background: #4c4c4ce3; height: 30px; width: 100%"> </div>' + '</br>' + '</br>' + \
                            'Nachricht von ' + vorname + ' ' + nachname + ':</strong>' + \
                            '</br>' + '</br>' + nachricht + '</br>' + '</span>'
			msg = EmailMultiAlternatives(
            	subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()

			x = 1
	return HttpResponse(x, content_type='text/html')



def websiteespenhain(request): 
	return render(request, 'websiteespenhain.html')


def loadpagetomail(request):
	if request.method == 'POST':
		subject = "Website Espenhain wurde besucht"
		subject, from_email, to = subject, 'anfrage@buchfinkmailservice.de', 'florian@buchfink.de'
		text_content = ''
		html_content = '<span> Website espenhain wurde besucht</span>'
		msg = EmailMultiAlternatives(
				subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()


		x=1
	return HttpResponse(x, content_type='text/html')
