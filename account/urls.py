from django.contrib.auth import views
from django.urls import path
from .views import ProductList, ProductCreate, CategoryCreate, CategoryList, ProductUpdate, ProductDelete, \
    CategoryDelete, ProfileView, CollectionList, CollectionCreate, CollectionDelete

app_name = 'account'

urlpatterns = [
    path('', ProductList.as_view(), name='dashboard'),
    path('product/create', ProductCreate.as_view(), name='product_create'),
    path('product/update/<int:pk>', ProductUpdate.as_view(), name='product_update'),
    path('product/delete/<int:pk>', ProductDelete.as_view(), name='product_delete'),
    path('category/', CategoryList.as_view(), name='category'),
    path('category/create', CategoryCreate.as_view(), name='category_create'),
    path('category/delete/<int:pk>', CategoryDelete.as_view(), name='category_delete'),
    path('collection/', CollectionList.as_view(), name='collection'),
    path('collection/create', CollectionCreate.as_view(), name='collection_create'),
    path('collection/delete/<int:pk>', CollectionDelete.as_view(), name='collection_delete'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
