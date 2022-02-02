import datetime
import xlwt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from products.models import Product
from .forms import UserOrderForm
from .models import Order, OrderDetail
from django.http import HttpResponse, FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


@login_required
def add_user_order(request):
    new_order_form = UserOrderForm(request.POST or None)

    if new_order_form.is_valid():
        order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if order is None:
            order = Order.objects.create(owner_id=request.user.id, is_paid=False)

        product_id = new_order_form.cleaned_data.get('product_id')
        count = new_order_form.cleaned_data.get('count')
        if count < 0:
            count = 1
        product = Product.objects.get_by_id(product_id=product_id)
        order.orderdetail_set.create(product_id=product_id, count=count)
        return redirect(f'/product/{product.id}/{product.slug}')

    return redirect('/')


@login_required
def user_open_order(request):
    context = {
        'order': None,
        'details': None,
    }
    open_order = Order.objects.filter(owner_id=request.user.id).first()
    if open_order is not None:
        context['order'] = open_order
        context['details'] = open_order.orderdetail_set.all()
    return render(request, 'order/user_open_order.html', context)


@login_required
def remove_item_order(request, *args, **kwargs):
    detail_id = kwargs.get('detail_id')
    if detail_id is not None:
        order_detail = OrderDetail.objects.get_queryset().get(id=detail_id, order__owner_id=request.user.id)
        if order_detail is not None:
            order_detail.delete()
        return redirect('order:open-order')


@login_required
def remove_all_order(request, *args, **kwargs):
    order_detail = OrderDetail.objects.all()
    if order_detail is not None:
        order_detail.delete()
    return redirect('order:open-order')


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=OrderDetail' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('OrderDetail', cell_overwrite_ok=True)
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['image', 'slug', 'parts', 'technique']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = OrderDetail.objects.filter(order__owner=request.user).values_list('product__image', 'product__slug',
                                                                             'product__parts', 'product__image')
    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response


def generate_pdf(request):
    open_order = Order.objects.filter(owner_id=request.user.id).first()
    context = {'order': open_order,
               'details': open_order.orderdetail_set.all(),
               }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orders.pdf"'

    # find the template and render it.
    template = get_template('order/pdf1.html')
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html.encode('utf-8'), dest=response, encodings='utf-8')

    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
