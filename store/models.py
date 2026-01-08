from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from categories.models import Category
from sub_categories.models import SubCategory
from django.urls import reverse
from account.models import Account
from django.db.models import Avg , Count
import os

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='photos/products', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('sub_categories.SubCategory', on_delete=models.CASCADE, null=True, blank=True)  # Made nullable
    created_at = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    product_feature_1 = models.CharField(max_length=30 , null=True ,  blank=True)
    product_feature_2 = models.CharField(max_length=30 , null=True ,  blank=True)
    product_feature_3 = models.CharField(max_length=30 , null=True ,  blank=True)


    def __str__(self):
        return self.product_name
    
    def average_review(self):
        reviews = ReviewProduct.objects.filter(product=self , status=True).aggregate(average=Avg('rating'))
        return reviews['average'] or 0
    
    def count_review(self):
        review = ReviewProduct.objects.filter(product=self , status=True).aggregate(count=Count('id'))
        return review['count'] or 0

    class Meta:
        ordering = ['product_name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        # Convert product_name to title case before saving
        self.product_name = self.product_name.title()
        if self.product_feature_1:  # Only if not None or empty
            self.product_feature_1 = self.product_feature_1.title()
        if self.product_feature_2:
            self.product_feature_2 = self.product_feature_2.title()
        if self.product_feature_3:
            self.product_feature_3 = self.product_feature_3.title()
        
        super().save(*args, **kwargs)

    def get_product_url(self):
        return reverse ('product_details' , args=[self.sub_category.slug , self.slug])

    def clean(self):
        # Optional: Add custom validation
        if self.price <= 0:
            raise ValidationError({'price': 'Price must be greater than zero.'})
        
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager , self).filter(variation_category='color' , is_active=True)
    def sizes(self):
        return super(VariationManager , self).filter(variation_category='size' , is_active=True)

variation_category_choice = (
    ('color' , 'color'),
    ('size' ,' size'),
)

class Variation(models.Model):

    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100 , choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , default=None)
    image = models.ImageField(upload_to='store/products' , max_length=255)

    def __srt__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'

class ReviewProduct(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    user = models.ForeignKey(Account , on_delete=models.CASCADE)
    subject = models.CharField(max_length=150 , blank=True)
    review = models.TextField(max_length=500 , blank=True)
    rating = models.IntegerField()
    ip = models.CharField(max_length=20 , blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject