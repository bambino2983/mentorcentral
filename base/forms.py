from dataclasses import fields
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from django.forms import ModelForm
from .models import Kb

class KbForm(ModelForm):
    class Meta:
        model = Kb
        fields = '__all__'