from django.urls import path

from .views import Home, upload_file, ProjectAutocomplete
from CA_Django_connector.views import ProjectDashboardView


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("upload/", upload_file, name='upload'),
    path("projects-autocomplete/", ProjectAutocomplete.as_view(), name='projects-autocomplete')
]