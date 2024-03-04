from django import forms
from .models import MapExhibitContribution

import logging

logger = logging.getLogger("ifcollectors")

class MapExhibitContributionForm(forms.ModelForm):
    class Meta:
        model = MapExhibitContribution
        fields = ['recipe_name', 'recipe', 'cultural_connections', 'media']
    
    def __init__(self, *args, **kwargs):
        super(MapExhibitContributionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'