from django.urls import path

from .views import testing_map, MapExhibitContributionCreateView, UserSubmissions, kakuma

urlpatterns = [
    path("exhibits/syria_recipes_and_cultures/", testing_map, name="testing_map"),
    path("exhibits/syria_recipes_and_cultures/contrib", MapExhibitContributionCreateView.as_view(),
         name='map-contribute'),
    path("exhibits/kakuma/", kakuma, name="kakuma"),
    path("exhibits/submissions/", UserSubmissions.as_view(), name="submissions"),
]