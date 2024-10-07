from django import forms
from .models import Products

input_css_classes = "form-control"


class ProductForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ["name", "handle", "price"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": input_css_classes})
