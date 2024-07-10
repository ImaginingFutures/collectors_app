import os
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, ListView, DeleteView

from exhibits.models import Exhibit

# Create your views here.
from .models import (ExternalResource, Project, ProjectTypes, ProjectParticipant, Place, Themes, Keywords,
                     Rights, UploadFile, Records)
from .forms import (ExternalResourceForm, KeywordForm, PlaceForm, ProjectForm, ProjectParticipantForm, ThemeForm, UploadForm)

from dal import autocomplete

import logging

logger = logging.getLogger("ifcollectors")

## Home

class Home(TemplateView):
    template_name = 'CA_Django_connector/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        
        context['projects'] = Project.objects.all()
        context['exhibits'] = Exhibit.objects.all()

        return context

## Dashboards

class ProjectDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'CA_Django_connector/dashboard/project_manager.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['projects'] = Project.objects.filter(users=user)
        return context

## 

class ProjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Project.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
            
        return qs

class ProjectTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ProjectTypes.objects.all().order_by('project_type')
        if self.q:
            qs = qs.filter(project_type__icontains=self.q)
            
        return qs
    
class ProjectParticipantAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ProjectParticipant.objects.all().order_by('full_name')
        if self.q:
            qs = qs.filter(full_name__icontains=self.q)
            
        return qs
    
class PlaceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Place.objects.all().order_by('place_name')
        if self.q:
            qs = qs.filter(place_name__icontains=self.q)
            
        return qs

class ResourceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ExternalResource.objects.all()
        if self.q:
            qs = qs.filter(resource_name__icontains=self.q)
            
        return qs

class RightsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Rights.objects.all().order_by('license')
        if self.q:
            
            qs = qs.filter(
                Q(license__icontains=self.q) |
                Q(license_abreviation__icontains=self.q)
                )
            
        return qs

class ThemesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Themes.objects.all().order_by('theme')
        if self.q:
            qs = qs.filter(theme__icontains=self.q)
            
        return qs


class KeywordsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Keywords.objects.all().order_by('keyword')
        if self.q:
            qs = qs.filter(keyword__icontains=self.q)
            
        return qs

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'CA_Django_connector/manage/project.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})
    
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'CA_Django_connector/manage/project.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('CA_Django_connector.edit_project'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_has_perm_to_edit'] = True
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'edit'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        
        return kwargs
    
    def get_success_url(self) -> str:
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})

class ProjectDetailView(DetailView):
    model = Project
    template_name = "CA_Django_connector/detail/project.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        project = self.get_object()
        
        files = UploadFile.objects.filter(
            models.Q(
                project=project
            )
        )
        
        context['files'] = files
        context['themes'] = project.themes.all()
        context['keywords'] = project.keywords.all()
        context['users'] = project.users.all()
        context['participants'] = project.participants.all()
        context['countries_or_regions'] = project.country_or_region.all()
        context['external_resources'] = project.external_resources.all()
        
        history_records = self.object.history.all()
        context['history_records'] = history_records
        
        return context



class ProjectParticipantCreateView(CreateView):
    model = ProjectParticipant
    form_class = ProjectParticipantForm
    template_name = 'CA_Django_connector/modals/participant.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_participant'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'add'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['CA_Django_connector/modals/participant.html']
        return ['CA_Django_connector/manage/participant.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'id': self.object.id,
                'full_name': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        
        project_initial = self.request.GET.get('project')
        if project_initial:
            initial['project'] = project_initial
            
        return initial
    
class PlaceCreateView(CreateView):
    model = Place
    form_class = PlaceForm
    template_name = 'CA_Django_connector/modals/place.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_place'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'add'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['CA_Django_connector/modals/place.html']
        return ['CA_Django_connector/manage/place.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'id': self.object.id,
                'place_name': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)
    
    
class ResourceCreateView(CreateView):
    model = ExternalResource
    form_class = ExternalResourceForm
    template_name = 'CA_Django_connector/modals/resource.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_resource'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'add'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['CA_Django_connector/modals/resource.html']
        return ['CA_Django_connector/manage/resource.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'id': self.object.id,
                'resource_name': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)
    
    
class ThemeCreateView(CreateView):
    model = Themes
    form_class = ThemeForm
    template_name = 'CA_Django_connector/modals/theme.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_theme'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'add'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['CA_Django_connector/modals/theme.html']
        return ['CA_Django_connector/manage/theme.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'id': self.object.id,
                'theme': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)
    
class KeywordCreateView(CreateView):
    model = Keywords
    form_class = KeywordForm
    template_name = 'CA_Django_connector/modals/keyword.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_keyword'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'add'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['CA_Django_connector/modals/keyword.html']
        return ['CA_Django_connector/manage/keyword.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'id': self.object.id,
                'keyword': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)


class RightsBrowse(ListView):
    model = Rights
    template_name = "CA_Django_connector/browse/rights.html"
    
    
## Files management

TYPES = [
    'image/jpeg', 'image/png', 'image/tiff', 'image/gif', 'image/bmp', 'image/webp', 
    'video/mp4', 'video/webm', 'video/ogg', 'video/quicktime', 'audio/mpeg', 'audio/mp4', 'audio/ogg', 
    'audio/wav', 'application/pdf', 'application/msword', 
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
    'application/vnd.ms-excel', 
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
    'application/vnd.ms-powerpoint', 
    'application/vnd.openxmlformats-officedocument.presentationml.presentation', 
    'text/plain', 'text/csv', 'text/xml', 'model/gltf-binary', 'application/zip',
    'application/x-zip-compressed', 'application/x-compressed', 'multipart/x-zip'
]

def validate_files(uploaded_file, allowed_types=TYPES):
    if uploaded_file.content_type not in allowed_types:
        return False, "File type is not allowed."
    return True, 'Valid'

# views.py
def upload_file(request, pk=None):
    project = None
    context = {}
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            
            for key in request.FILES:
                file = request.FILES[key]
                logger.debug(f'File to upload: {file}')
                logger.debug(f'File to upload: {file}, MIME type: {file.content_type}')
                is_valid, message = validate_files(file)
                if not is_valid:
                    return JsonResponse({'error': message}, status=400)
                
                UploadFile.objects.create(project=project, file=file)
            return redirect('project_dashboard')
        else:
            logger.debug(f'Form errors: {form.errors}')
    else:
        if pk:
            project = get_object_or_404(Project, pk=pk)
            form = UploadForm(initial={'project': project})
            form.fields['project'].widget.attrs['readonly'] = True
            form.fields['project'].widget.attrs['disabled'] = True
        else:
            form = UploadForm()
    
    context['form'] = form
    context['project_id'] = pk
    context['project'] = project
    context['next_url'] = request.GET.get('next', '')
            
    return render(request, 'CA_Django_connector/files/upload.html', context)


class ProjectFilesView(ListView):
    model = UploadFile
    template_name = 'CA_Django_connector/files/project.html'
    context_object_name = 'files'

    def get_queryset(self):
        self.project = get_object_or_404(Project, id=self.kwargs['pk'])
        return UploadFile.objects.filter(project=self.project)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context
    

class FileDeleteView(DeleteView):
    model = UploadFile
    template_name = 'CA_Django_connector/common/confirm_delete.html'
    success_url = reverse_lazy('project_dashboard')  

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)

    def delete(self, request, *args, **kwargs):
        logger.debug("PReparing to delete file")
        self.object = self.get_object()
        file_path = self.object.file.path
        logger.debug(f"File path to delete {file_path}")
        response = super().delete(request, *args, **kwargs)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"File {file_path} deleted successfully")
        else:
            logger.debug(f"File {file_path} does not exist")
        return response
