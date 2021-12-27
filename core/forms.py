from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.forms import widgets
from django_countries.fields import Country, CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Review



class CheckoutForm(forms.Form):
    address1 = forms.CharField(required=False)
    address2= forms.CharField(required=False)
    country = CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    state = forms.CharField(required=False)
    zip = forms.CharField(required=False)
    default = forms.BooleanField(required=False)
    default_shipping_address = forms.BooleanField(required=False)

class SignupCreation(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['email','first_name','last_name']

class RatingForms(forms.Form):
    comment = forms.CharField(max_length=250)
    # comment = forms.CharField(widget=forms.Textarea(attrs={
    #     'class': 'md-textarea form-control pr-6',
    #     'placeholder': 'Type your comment',
    #     'id': 'form76',
    #     'rows': '4'
    # }))
    rate=forms.FloatField()
    # class Meta:
    #     model = Review
    #     fields = ['comment']