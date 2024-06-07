from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Article
from .forms import ArticleForm

class ArticleListView(ListView):
    model = Article
    paginate_by = 10  # Adjust the number of articles per page

class ArticleDetailView(DetailView):
    model = Article

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'collected/article_form.html'

class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'collected/article_form.html'
