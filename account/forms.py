from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class ProfileForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ProfileForms, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None

        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['phone'].disabled = True
            self.fields['is_author'].disabled = True

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'is_author']


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')
        
        
class OtpForm(forms.Form):
    otp_code = forms.CharField(max_length=4)