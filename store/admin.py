from django.contrib import admin
from .models import Product , Variation

class StoreAdmin(admin.ModelAdmin):
    list_display = ('product_name' , 'price' , 'stock' , 'category' , 'modify_date' , 'is_available')
    search_fields = ('product_name' ,)
    list_filter = ('modify_date' ,)

    prepopulated_fields = {
        'slug':('product_name',)
    }

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product' , 'variation_category' , 'variation_value' , 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product' , 'variation_category' , 'variation_value')

admin.site.register(Product , StoreAdmin)
admin.site.register(Variation , VariationAdmin)