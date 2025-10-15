from django.contrib import admin
from .models import Product

class StoreAdmin(admin.ModelAdmin):
    list_display = ('product_name' , 'price' , 'stock' , 'category' , 'modify_date' , 'is_available')
    search_fields = ('product_name' ,)
    list_filter = ('modify_date' ,)

    prepopulated_fields = {
        'slug':('product_name',)
    }

admin.site.register(Product , StoreAdmin)