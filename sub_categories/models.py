from django.db import models

class SubCategory(models.Model):
    sub_category_name   = models.CharField(max_length=50 , unique= True)
    slug                = models.SlugField(max_length=100 , unique=True)
    description         = models.TextField(max_length=255 , blank= True)
    cat_image           = models.ImageField(upload_to="photos/categories" , blank=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "sub_categories"


    def __str__(self):
        return self.sub_category_name