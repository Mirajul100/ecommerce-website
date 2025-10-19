from django.contrib import admin
from .models import SubCategory

class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('sub_category_name',)
    }

    list_display = ('sub_category_name' , 'slug')
    search_fields = ('sub_category_name',)

admin.site.register(SubCategory , SubCategoryAdmin)
