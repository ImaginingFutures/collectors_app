from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.models import User
from .forms import UploadForm
from .models import UploadFile
from CA_Django_connector.models import Project
from exhibits.models import Exhibit

from dal import autocomplete

import logging

logger = logging.getLogger("ifcollectors")

# Create your views here.

## Custom validators

TYPES = ['image/jpeg', ' image/png', ' image/tiff', ' image/gif', ' image/bmp', ' image/webp', ' video/mp4', ' video/webm', ' video/ogg', ' audio/mpeg', ' audio/mp4', ' audio/ogg', ' audio/wav', ' application/pdf', ' application/msword', ' application/vnd.openxmlformats-officedocument.wordprocessingml.document', ' application/vnd.ms-excel', ' application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', ' application/vnd.ms-powerpoint', ' application/vnd.openxmlformats-officedocument.presentationml.presentation', ' text/plain', ' text/csv', ' text/xml']

def validate_files(uploaded_file, allowed_types=TYPES):
    """
    Validate the uploaded file's type and size.
    
    Args:
        uploaded_file: The uploaded file to validate.
        max_size: Maximum file size in bytes.
        allowed_types: List of allowed MIME types.
        
    Returns:
        bool: True if the file is valid, False otherwise.
    """
    
    if uploaded_file.content_type not in allowed_types:
        return False, "File type is not allowed."
    
    return True, 'Valid'



## autocompletions

class ProjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Project.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
            
        return qs


class Home(TemplateView):
    template_name = 'filebox/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        
        context['projects'] = Project.objects.all()
        context['exhibits'] = Exhibit.objects.all()

        return context
    


def upload_file(request):

    if request.method == 'POST':
        
        form = UploadForm(request.POST)
        
        if form.is_valid():
            project = form.cleaned_data['project']
            
            for key in request.FILES:
                file = request.FILES[key]
                logger.debug(f'File to upload: {file}')
                is_valid, message = validate_files(file)
                if not is_valid:
                    return JsonResponse({'error': message}, status=400)
                
                UploadFile.objects.create(project=project, file=file)
                
            return redirect('home')    
        else:
            logger.debug(f'Form errors: {form.errors}')
    else:
        form = UploadForm()
            
    return render(request, 'filebox/myproject/upload.html', {'form': form})