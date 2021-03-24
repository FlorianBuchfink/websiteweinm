from django.urls import path 
from xxxwebsite2.views import (
    sendkontaktformular, index, websiteespenhain, loadpagetomail)

urlpatterns = [
	path('loadpagetomail/', loadpagetomail, name='loadpagetomail'),
	path('websiteespenhain', websiteespenhain, name='websiteespenhain'),
	path('sendkontaktformular/', sendkontaktformular, name='sendkontaktformular'),
	path('', index, name='index'), 
]
