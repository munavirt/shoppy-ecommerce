from django.db import models
from category.models import Category 
from django.urls import reverse
from django.utils.html import mark_safe


from accounts.models import Account


# Create your models here.
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500,blank=True)
    price           = models.FloatField()
    images          = models.ImageField(upload_to='photos/prodcuts')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    is_featured     = models.BooleanField(default=False)
    
    
    def get_url(self):
        return reverse('product_details', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name
    
    def is_stock_zero(self):
        if self.stock == 0:
            return mark_safe('<a href="{}">{} - out of stock</a>'.format(self.get_url(), self.product_name))
        return ''
    


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    
    

    
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.subject
    
    

class Banner(models.Model):
    banner_name    = models.CharField(max_length=200, unique=True)
    b_description     = models.TextField(max_length=500,blank=True)
    price           = models.FloatField()
    b_images          = models.ImageField(upload_to='photos/banners')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    
  
    def __str__(self):
        return self.banner_name
    
    def get_related_products(self):
        if self.is_available:
            related_products = Product.objects.filter(
                product_name__startswith=self.banner_name
            )
            return related_products
        return None
    
    
class ProductGallery(models.Model):
    
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)
    
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
        
        