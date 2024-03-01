from django import forms
from .models import UploadFile
from CA_Django_connector.models import Project

from dal import autocomplete

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        exclude = ('file',)
        
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=autocomplete.ModelSelect2(url='projects-autocomplete')
    )