from django.shortcuts import render
from django.views.generic import TemplateView
from books.models import CreateBook, CreateCategory

# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self,*args,**kwargs):
        context =  super().get_context_data(*args,**kwargs)
        context['books'] = CreateBook.objects.all()
        context['categories'] = CreateCategory.objects.all()
        return context

class HomeCategoryView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self,*args,**kwargs):
        context =  super().get_context_data(*args,**kwargs)
        category_slug = self.kwargs['category_slug']
        category = CreateCategory.objects.get(slug=category_slug)
        context['categories'] = CreateCategory.objects.all()
        context['books'] = CreateBook.objects.filter(categories=category)
        return context