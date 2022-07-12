from dataclasses import fields
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from django.forms import ModelForm
from .models import Kb, User

class KbForm(ModelForm):
    class Meta:
        model = Kb
        fields = '__all__'
        exclude = ['creator', 'partners']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email'] 