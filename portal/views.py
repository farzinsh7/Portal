from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from products.models import Category, Collection


class HomeView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'portal/index.html'
    queryset = Category.objects.filter(status=True)


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    paginate_by = 3
    template_name = 'product/category.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.all(), slug=slug)
        return category.product.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(status=True)
        return context


class CollectionList(LoginRequiredMixin, ListView):
    model = Collection
    paginate_by = 6
    template_name = 'product/collection.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        collection = get_object_or_404(Collection.objects.all(), slug=slug)
        return collection.product.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection'] = Collection.objects.all()
        return context
