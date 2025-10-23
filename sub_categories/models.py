from django.db import models
from django.urls import reverse
from categories.models import Category

class SubCategory(models.Model):
    sub_category_name   = models.CharField(max_length=50 , unique= True)
    slug                = models.SlugField(max_length=100 , unique=True)
    description         = models.TextField(max_length=255 , blank= True)
    cat_image           = models.ImageField(upload_to="photos/categories" , blank=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "sub_categories"

    def save(self, *args, **kwargs):
        # Convert sub_category_name to title case before saving
        self.sub_category_name = self.sub_category_name.title()
        super().save(*args, **kwargs)

    def get_sub_category_url(self):
        return reverse('sub_category' , args= [self.slug])

    def __str__(self):
        return self.sub_category_name