from django.urls import path

from .views import (ProjectCreateView, ProjectUpdateView, ProjectTypeAutocomplete, ProjectParticipantAutocomplete,
                    ProjectParticipantCreateView, PlaceCreateView, ResourceCreateView, RightsBrowse,
                    ThemeCreateView, KeywordCreateView, ProjectDetailView,
                    PlaceAutocomplete, ThemesAutocomplete, KeywordsAutocomplete, ResourceAutocomplete,
                    ProjectDashboardView, RightsAutocomplete)

urlpatterns = [
    path("Dashboard/projects/", ProjectDashboardView.as_view(), name="project_dashboard"),
    path("Create/participant/", ProjectParticipantCreateView.as_view(), name="create_participant"),
    path("Create/project/", ProjectCreateView.as_view(), name="create_project"),
    path("Create/place/", PlaceCreateView.as_view(), name="create_place"),
    path("Create/resource/", ResourceCreateView.as_view(), name="create_resource"),
    path("Create/theme/", ThemeCreateView.as_view(), name="create_theme"),
    path("Create/keyword/", KeywordCreateView.as_view(), name="create_keyword"),
    path("Update/project/<int:pk>/", ProjectUpdateView.as_view(), name="update_project"),
    path("Detail/project/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("Browse/rights/", RightsBrowse.as_view(), name="rights_browse"),
    path("typeproject-autocomplete", ProjectTypeAutocomplete.as_view(), name="typeproject-autocomplete"),
    path('projectparticipant-autocomplete', ProjectParticipantAutocomplete.as_view(), name="projectparticipant-autocomplete"),
    path("place-autocomplete", PlaceAutocomplete.as_view(), name="place-autocomplete"),
    path("themes-autocomplete", ThemesAutocomplete.as_view(), name="themes-autocomplete"),
    path("rights-autocomplete", RightsAutocomplete.as_view(), name="rights-autocomplete"),
    path("keywords-autocomplete", KeywordsAutocomplete.as_view(), name="keywords-autocomplete"),
    path("resource-autocomplete", ResourceAutocomplete.as_view(), name='resource-autocomplete')
]
