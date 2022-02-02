from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from products.models import Product


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ['title', 'author', 'parts', 'slug', 'category', 'collection', 'description', 'image', 'image_1',
                           'model_3dm',
                           'model_3dm_1', 'model_stl', 'model_stl_1', 'publish', 'status', 'color', 'technique']
        elif request.user.is_author:
            self.fields = ['title', 'parts', 'slug', 'category', 'collection', 'description', 'image', 'image_1',
                           'model_3dm',
                           'model_3dm_1', 'model_stl', 'model_stl_1', 'publish', 'status', 'color', 'technique']
        else:
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        if product.author == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("account:profile")
        else:
            return redirect('login')


class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


class AuthorAccessPreviewMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        if product.author == request.user and product.status == 'd' or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
