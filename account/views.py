from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from products.models import Product, Category, Collection
from .forms import ProfileForms
from .mixins import FieldsMixin, FormValidMixin, AuthorAccessMixin, SuperUserAccessMixin, AuthorsAccessMixin
from .models import User
from django.contrib.auth.views import LoginView, PasswordChangeView


class ProductList(AuthorsAccessMixin, ListView):
    template_name = 'dashboard.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        else:
            return Product.objects.filter(author=self.request.user)


class ProductCreate(AuthorsAccessMixin, FormValidMixin, FieldsMixin, CreateView):
    model = Product
    template_name = 'registration/product-create-update.html'


class ProductUpdate(AuthorAccessMixin, FormValidMixin, FieldsMixin, UpdateView):
    model = Product
    template_name = 'registration/product-create-update.html'


class ProductDelete(AuthorAccessMixin, SuperUserAccessMixin, FormValidMixin, FieldsMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('account:dashboard')
    template_name = 'registration/product_confirm_delete.html'


class CategoryList(LoginRequiredMixin, ListView):
    template_name = 'registration/category-list.html'
    queryset = Category.objects.all()


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['title', 'slug', 'status', 'image']
    template_name = 'registration/category-create.html'


class CategoryDelete(AuthorAccessMixin, SuperUserAccessMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('account:category')
    template_name = 'registration/product_confirm_delete.html'


class CollectionList(LoginRequiredMixin, ListView):
    template_name = 'registration/collection-list.html'
    queryset = Collection.objects.all()


class CollectionCreate(LoginRequiredMixin, CreateView):
    model = Collection
    fields = ['title', 'slug']
    template_name = 'registration/collection-create.html'


class CollectionDelete(AuthorAccessMixin, SuperUserAccessMixin, FormValidMixin, FieldsMixin, DeleteView):
    model = Collection
    success_url = reverse_lazy('account:collection')
    template_name = 'registration/product_confirm_delete.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('account:profile')
    form_class = ProfileForms

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy("account:dashboard")
        else:
            return reverse_lazy("account:profile")


from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعالسازی اکانت'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('لطفا برا تکمیل عملیات ثبت نام ایمیل خود را تایید کنید.')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return HttpResponse('ایمیل شما تایید شد. برای ورد <a href="/login">کلیک </a>کنید.')
    else:
        return HttpResponse('لینک فعالسازی نامعتبر است! <a href="/register">دوباره امتحان کنید</a>')