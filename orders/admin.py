from django.contrib import admin
from .models import Payment , Order , OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    can_delete = False
    extra = 0

    fields = (
        'payment',
        'user',
        'product',
        'quantity',
        'product_price',
    )

    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False



class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number' , 'full_name' , 'phone_number' , 'email' , 'city' , 'order_total' , 'tax' , 'status' , 'is_ordered' , 'created_at']
    list_filter = ['status' , 'is_ordered']
    search_fields = ['order_number' , 'first_name' , 'last_name' , 'phone_number' , 'email']
    list_per_page = 20
    inlines = [OrderProductInline]

class OrderPayment(admin.ModelAdmin):
    list_display = ['user' , 'payment_id' , 'payment_method' , 'amount_paid' , 'created_at']
    list_filter = ['payment_method',]
    search_fields = ['user__email',]
    list_per_page = 20

admin.site.register(Payment , OrderPayment)
admin.site.register(Order , OrderAdmin)
admin.site.register(OrderProduct)