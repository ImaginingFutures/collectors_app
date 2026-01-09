from typing import Any
from django.db.models.query import QuerySet, Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponse, Http404
from django.views import View
from .models import Article
from .forms import ArticleForm
from CA_Django_connector.models import (
    ProjectParticipant, Project, Keywords
)
import logging

logger = logging.getLogger("ifcollectors")

class ArticleListView(ListView):
    model = Article
    paginate_by = 10 
    template_name = 'collected/article_list.html'
    context_object_name = 'articles'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(authors__full_name__icontains=query) |
                Q(contentHTML__icontains=query)
            ).distinct()
            
        # Filter by authors
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(authors__id=author)
            
        # Filter by projects
        project = self.request.GET.get('project')
        if project:
            queryset = queryset.filter(projects__id=project)
            
        # Filter by keywords
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(keywords__id=keyword)
            
        return queryset.distinct()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context['authors'] = ProjectParticipant.objects.filter(
            article__in=Article.objects.all()
        ).distinct()
        context['projects'] = Project.objects.filter(
            article__in=Article.objects.all()
        ).distinct()
        context['keywords'] = Keywords.objects.filter(
            article__in=Article.objects.all()
        ).distinct()
        
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'collected/article_detail.html'
    context_object_name = 'article'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        names_objects = self.object.authors.all()
        names = [nameo.full_name for nameo in names_objects]
        sorted_names = sorted(names, key=lambda name: name.split()[-1])
        
        context['ordered_authors'] = sorted_names
        
        return context


class ArticleDetailHTMLView(DetailView):
    model = Article
    template_name = 'collected/article_detail_html.html'
    context_object_name = 'article'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        names_objects = self.object.authors.all()
        names = [nameo.full_name for nameo in names_objects]
        sorted_names = sorted(names, key=lambda name: name.split()[-1])
        
        context['ordered_authors'] = sorted_names
        
        return context

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'collected/article_form.html'

class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'collected/article_form.html'


class ArticlePDFProxyView(View):
    """
    Proxy view to serve PDFs from S3 through Django.
    This solves PDF.js cross-origin issues by serving PDFs from the same domain.
    """
    
    def get(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            
            if not article.filePDF:
                raise Http404("PDF not found")
            
            # Open the file from S3
            pdf_file = article.filePDF.open('rb')
            
            # Create response with PDF content
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{article.filePDF.name.split("/")[-1]}"'
            response['Accept-Ranges'] = 'bytes'
            
            # Add CORS headers for safety
            response['Access-Control-Allow-Origin'] = '*'
            
            pdf_file.close()
            return response
            
        except Article.DoesNotExist:
            raise Http404("Article not found")
        except Exception as e:
            logger.error(f"Error serving PDF for article {pk}: {e}")
            raise Http404("Error loading PDF")
