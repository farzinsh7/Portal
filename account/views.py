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



import random
import threading
import time
from django.shortcuts import redirect
from django.views.generic import FormView
from django.contrib.auth import login
from .forms import SignupForm, OtpForm
from django.contrib import messages
from melipayamak import Api
from decouple import config



class OTPService:
    def __init__(self):
        self.username = config('USERNAME_PANEL')
        self.password = config('PASSWORD_PANEL')
        self._from = config('FROM_PANEL')
        self.api = Api(self.username, self.password)
        
    def generate_code(self):
        return random.randint(1000, 9999)
    
    def send_otp(self, phone_number, code):
        sms = self.api.sms()
        text = f"OTP Code: {code}"
        response = sms.send(to=phone_number, _from=self._from, text=text)
        print(response)
        return response
    

    
class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.otp_service = OTPService()

    def delete_code(self):
        time.sleep(10)
        self.request.session.pop('code', None)
        self.request.session.save()

    def form_valid(self, form):
        self.request.session['user_data'] = form.cleaned_data
        self.request.session.save()

        code = self.otp_service.generate_code()
        self.request.session['code'] = code

        to = str(self.request.session['user_data']['phone'])
        

        self.otp_service.send_otp(phone_number=to, code=code)


        tr1 = threading.Thread(target=self.delete_code)
        tr1.start()

        return redirect("otp-verify")



class OtpVerifyView(FormView):
    template_name = "registration/otp.html"
    form_class = OtpForm
    success_url = reverse_lazy("account:dashboard")
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize OTPService
        self.otp_service = OTPService()

    def form_valid(self, form):
        code = self.request.POST['otp_code']
        
        if self.request.session.get('code') and int(code) == self.request.session['code']:
            # Process the user data as before
            user_data = self.request.session.get('user_data')
            if user_data:
                password = user_data.pop('password1')
                user_data.pop('password2', None)
                
                user = User(**user_data)
                user.is_author = True
                user.set_password(password)
                user.save()
                
                login(self.request, user)
                
                self.request.session.pop('user_data', None)
                self.request.session.pop('code', None)

            return redirect(self.success_url)
        else:
            messages.error(self.request, "The OTP code is incorrect. Please try again.")
            return redirect("otp-verify")

    def post(self, request, *args, **kwargs):
        if "resend_otp" in request.POST:
            # Resend OTP logic
            code = random.randint(1000, 10000)
            request.session['code'] = code
            
            # Generate and store OTP code in session
            code = self.otp_service.generate_code()
            self.request.session['code'] = code

            # Get the phone number from session user data
            to = str(self.request.session['user_data']['phone'])
            
            # Send OTP
            self.otp_service.send_otp(phone_number=to, code=code)

            messages.success(request, "A new OTP code has been sent.")
            return self.get(request, *args, **kwargs)  # Reload the page

        return super().post(request, *args, **kwargs)