from django.urls import path
from . import views

urlpatterns = [
    path('place_order/' , views.place_order , name='place_order'),
    path('payment/<str:order_number>/' , views.payment , name='payment'),
    path('payment-success/', views.payment_success , name='payment_success'),
    path('payment-failed/', views.payment_failed , name='payment_failed'),
    path('payment-cancel/', views.payment_cancel , name='payment_cancel'),
    path('payment-ipn/', views.payment_ipn , name='payment_ipn'),
    path('order_completed/<str:order_number>/', views.order_completed, name='order_completed'),
    path('cash_on_delivery/<str:order_number>/' , views.cash_on_delivery, name='cash_on_delivery'),
]
