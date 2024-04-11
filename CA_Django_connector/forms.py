from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from dal import autocomplete
from .models import ExternalResource, Keywords, Place, Project, ProjectTypes, ProjectParticipant, Themes

class ProjectParticipantForm(forms.ModelForm):
    class Meta:
        model = ProjectParticipant
        fields = ['full_name', 'email', 'project_role']
        
    def __init__(self, *args, **kwargs):
        super(ProjectParticipantForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.fields.TypedChoiceField):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class ExternalResourceForm(forms.ModelForm):
    class Meta:
        model = ExternalResource
        fields = '__all__'
    
    url = forms.URLField(max_length=100, required=True)
        
    def __init__(self, *args, **kwargs):
        super(ExternalResourceForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Themes
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ThemeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keywords
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(KeywordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'

    lat = forms.DecimalField(max_digits=9, decimal_places=6, required=False)
    lon = forms.DecimalField(max_digits=9, decimal_places=6, required=False)
    
    
    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get('lat')
        lon = cleaned_data.get('lon')
        
        if (lat is not None and lon is None) or (lat is None and lon is not None):
            raise forms.ValidationError("Both latitude and longitude are required together.")

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = '__all__'
        
    
    name = forms.CharField(max_length=200, required=True)
    #project_description = forms.CharField(widget=CKEditor5Widget(config_name='extends'), required=False)
    #project_description_second = forms.CharField(widget=CKEditor5Widget(config_name='extends'), required=False)
    type_of_project = forms.ModelChoiceField(
        queryset=ProjectTypes.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='typeproject-autocomplete'),
        label='Project Type'
    )
    
    participants = forms.ModelMultipleChoiceField(
        queryset=ProjectParticipant.objects.all(),
        required=True,
        widget=autocomplete.ModelSelect2Multiple(url='projectparticipant-autocomplete'),
        label='Project Leaders'
    )
    
    country_or_region = forms.ModelMultipleChoiceField(
        queryset=Place.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(url='place-autocomplete'),
        label="Place"
    )
    
    external_resources = forms.ModelMultipleChoiceField(
        queryset=ExternalResource.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(url='resource-autocomplete'),
        label="External Resource"
    )
    
    themes = forms.ModelMultipleChoiceField(
        queryset=Themes.objects.all(),
        required=True,
        widget=autocomplete.ModelSelect2Multiple(url='themes-autocomplete'),
        label="Themes"
    )
    
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keywords.objects.all(),
        required=True,
        widget=autocomplete.ModelSelect2Multiple(url='keywords-autocomplete'),
        label="Keywords"
    )
    
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
                
        if self.instance and self.instance.pk:
            self.fields['project_idno'].widget = forms.HiddenInput()
            self.fields['type_of_project'].widget = forms.HiddenInput()
        
        if self.instance.pk:
            self.fields['users'].initial = self.instance.users.all()
            
        self.fields['users'].widget = forms.MultipleHiddenInput()
        
        if self.instance and self.instance.pk and self.instance.thumbnail:
            self.fields['thumbnail'].widget = forms.FileInput()
            self.current_thumbnail_url = self.instance.thumbnail.url
        else:
            self.current_thumbnail_url = None
            
        for field_name, field in self.fields.items():
            if isinstance(field, forms.fields.TypedChoiceField):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
                