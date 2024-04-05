from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView

# Create your views here.
from .models import (ExternalResource, Project, ProjectTypes, ProjectParticipant, Place, Themes, Keywords)
from .forms import (ExternalResourceForm, KeywordForm, PlaceForm, ProjectForm, ProjectParticipantForm, ThemeForm)

from dal import autocomplete

## Dashboards

class ProjectDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'CA_Django_connector/dashboard/project_manager.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['projects'] = Project.objects.filter(users=user)
        return context

## 

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
