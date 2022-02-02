from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from order.forms import UserOrderForm
from products.models import Product, Category, Collection
from account.mixins import AuthorAccessPreviewMixin
from django.contrib.auth.decorators import login_required


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/products-list.html'
    queryset = Product.objects.filter(status='p')
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # selected_product_id = kwargs['productId']
        context['category'] = Category.objects.filter(status=True)
        context['collection'] = Collection.objects.all()
        context['new-order'] = UserOrderForm(self.request.POST or None)
        return context


@login_required
def product_detail_view(request, slug, *args, **kwargs):
    selected_product_id = kwargs['productId']
    new_order_form = UserOrderForm(request.POST or None, initial={'product_id': selected_product_id})
    product = get_object_or_404(Product, slug=slug, status='p')
    category = Category.objects.filter(status=True)
    context = {
        'product': product,
        'category': category,
        'new_order': new_order_form,
    }
    return render(request, 'product/product-detail.html', context)


# def product_detail_preview(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     category = Category.objects.filter(status=True)
#     context = {
#         'product': product,
#         'category': category,
#     }
#     return render(request, 'product/product-detail.html', context)


class ProductPreview(AuthorAccessPreviewMixin, DetailView):
    template_name = 'product/product-detail.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Product, pk=pk)


class SearchList(LoginRequiredMixin, ListView):
    template_name = 'product/search_list.html'
    paginate_by = 9

    def get_queryset(self):
        search = self.request.GET.get('q')
        return Product.objects.filter(
            Q(description__icontains=search) | Q(title__icontains=search) | Q(slug__icontains=search) | Q(
                color__icontains=search), status='p')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context
