from django.urls import path
from .views import add_user_order, user_open_order, remove_item_order, export_excel, generate_pdf,remove_all_order

app_name = 'order'
urlpatterns = [
    path('order', add_user_order, name='new-order'),
    path('open-order', user_open_order, name='open-order'),
    path('remove-order/<detail_id>', remove_item_order, name='remove-order'),
    path('remove-all-order/', remove_all_order, name='remove-all-order'),
    path('export_excel', export_excel, name='export-excel'),
    path('export_pdf', generate_pdf, name='export-pdf'),
]
