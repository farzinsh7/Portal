from django.urls import path
from .views import HomeView, CategoryList, CollectionList

app_name = 'portal'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:slug>', CategoryList.as_view(), name='category'),
    path('collection/<slug:slug>', CollectionList.as_view(), name='collection'),
]
