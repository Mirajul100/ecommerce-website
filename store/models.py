from django.db import models
from categories.models import Category

class Product (models.Model):

    product_name        = models.CharField(max_length=200 , unique=True)
    slug                = models.SlugField(max_length=200 , unique=True)
    description         = models.TextField(max_length=200 , blank= True)
    price               = models.IntegerField()
    stock               = models.IntegerField()
    image               = models.ImageField(upload_to='photos/products')
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category , on_delete=models.CASCADE)
    create_date         = models.DateTimeField(auto_now_add= True)
    modify_date         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
