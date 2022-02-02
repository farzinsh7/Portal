from django.urls import path
from .views import ProductList, product_detail_view, ProductPreview, SearchList

app_name = 'product'
urlpatterns = [
    path('product/', ProductList.as_view(), name='product_list'),
    path('product/<productId>/<slug:slug>', product_detail_view, name='product_detail'),
    path('preview/<int:pk>', ProductPreview.as_view(), name='product_preview'),
    path('search', SearchList.as_view(), name='search'),
    path('search/page/<int:page>', SearchList.as_view(), name='search'),
]