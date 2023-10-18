from django import forms
from store.models import Product

class productForm(forms.ModelForm):
    class Meta:
         model = Product
         fields = ['product_name', 'slug', 'description', 'price', 'images', 'stock',
                      'is_available', 'is_featured', 'category', ]
        
    def __init__(self, *args, **kwargs):
        super(productForm,self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['min'] = 0
        self.fields['stock'].widget.attrs['min'] = 0
        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['is_available'].widget.attrs['type'] = 'checkbox'
        self.fields['is_featured'].widget.attrs['type'] = 'checkbox'
        self.fields['is_available'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_featured'].widget.attrs['class'] = 'form-check-input'