from django import forms
from .models import Product_Review, Address


Product_Rating = (
    ('1', '★☆☆☆☆'),
    ('2', '★★☆☆☆'),
    ('3', '★★★☆☆'),
    ('4', '★★★★☆'),
    ('5', '★★★★★'),
)


class Product_Review_Form(forms.ModelForm):
    class Meta:
        model = Product_Review
        fields = ['rating', 'review']

    review = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control my-3 py-1 rounded rounded-3',
        'placeholder': 'Review..'
    }))

    rating = forms.ChoiceField(choices=Product_Rating, widget=forms.Select(attrs={
        'class': 'form-select my-3 py-1 rounded rounded-3',
    }))


class Address_Form(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'contact', 'email', 'default_address']

    address = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Address',
        'class': 'form-area my-2 p-2 rounded rounded-3',
        'cols': 45,
        'rows': 6
    }))

    contact = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Contact No:',
        'class': 'form-control my-2 py-2 rounded rounded-3'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'e-Mail',
        'class': 'form-control my-2 py-2 rounded rounded-3'
    }))

    default_address = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }), required=False)
