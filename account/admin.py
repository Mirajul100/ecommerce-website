from django.contrib import admin
from .models import Account , UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

class AccountManager(UserAdmin):
    list_display = ('email' , 'first_name' , 'last_name' , 'last_login' , 'date_joined' , 'is_active')
    list_display_links = ('email' , 'first_name' , 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login' , 'date_joined')
    search_fields = ('email' , 'first_name' , 'last_name')
    
    filter_horizontal = ()
    list_filter = ('last_login' ,)
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

    def thumbnail(self, obj):
        # This is create automatic user profile
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="30" height="30" style="border-radius:50%; object-fit:cover;" />',
                obj.profile_picture.url
            )
        return format_html('<span style="color: #999;">No Image</span>')

    thumbnail.short_description = 'Profile Picture'

admin.site.register(Account , AccountManager)
admin.site.register(UserProfile , UserProfileAdmin)