from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from categories.models import Category
from sub_categories.models import SubCategory

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

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['product_name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def clean(self):
        # Optional: Add custom validation
        if self.price <= 0:
            raise ValidationError({'price': 'Price must be greater than zero.'})
