from datetime import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils import formats

from xxxwebsite2.CustomForms import appwidgets

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginAuthenticationForm(AuthenticationForm):
    """
    Abgeleitete Klasse aus AuthenticationForm für angepasste Darstellung der
    Login-Page.
    """

    username = UsernameField(
        label="",
        widget=appwidgets.myTextWidget(
            attrs={
                "autofocus": True,
                "class": "col-12",
                "placeholder": "Benutzer",
                "style": "height: 40px",
                "autocomplete": "off",
            }
        ),
    )

    password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Passwort",
                "class": "col-12",
                "style": "height: 40px",
                "autocomplete": "off",
            }
        ),
    )


class sendkontaktformularForm(forms.Form):

	vorname = forms.CharField(
		widget=appwidgets.myTextWidget(),
		localize=True,
		required=False,
	)

	nachname = forms.CharField(
		widget=appwidgets.myTextWidget(),
		localize=True,
		required=False,
	)

	email = forms.CharField(
		widget=appwidgets.myTextWidget(),
		localize=True,
		required=False,
	)

	telefon = forms.CharField(
		widget=appwidgets.myTextWidget(),
		localize=True,
		required=False,
	)

	nachricht = forms.CharField(
		widget=appwidgets.myTextWidget(),
		localize=True,
		required=False,
	)

	#placeForAnotherForms###RandomKey:cjlddlxpxa
