from django.urls import path

from .views import testing_map

urlpatterns = [
    path("exhibits/syria_recipes_and_cultures", testing_map, name="testing_map"),
]