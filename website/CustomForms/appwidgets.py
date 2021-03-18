from django.forms import widgets


class myTextWidget(widgets.TextInput):
    input_type = 'text'
    template_name = 'django/forms/widgets/text.html'


class DateFieldForm(widgets.TextInput):
    input_type = 'text'
