from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

class AccountManager(UserAdmin):
    list_display = ('email' , 'first_name' , 'last_name' , 'last_login' , 'date_joined' , 'is_active')
    list_display_links = ('email' , 'first_name' , 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login' , 'date_joined')
    search_fields = ('email' , 'first_name' , 'last_name')
    
    filter_horizontal = ()
    list_filter = ('last_login' ,)
    fieldsets = ()

admin.site.register(Account , AccountManager)