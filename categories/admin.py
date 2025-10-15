from django.contrib import admin
from .models import Category

class CategoryAdmin (admin.ModelAdmin):
    prepopulated_fields = {
        'slug':('Category_name' ,)
    }

    list_display = ('Category_name' , 'slug')
    search_fields = ('Category_name',)
    

admin.site.register(Category , CategoryAdmin)
