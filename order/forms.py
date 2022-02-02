from django import forms


class UserOrderForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    count = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
