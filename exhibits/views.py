from django.shortcuts import render

# Create your views here.

def testing_map(request):
    return render(request, 'exhibits/Maps/syria_recipes_and_cultures.html') 