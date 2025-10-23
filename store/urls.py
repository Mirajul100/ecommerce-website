from django.urls import path
from . import views

urlpatterns = [
    path("" , views.store , name="store"),
    path("<slug:sub_category_slug>/" , views.store , name="sub_category"),
    path("<slug:sub_category_slug>/<slug:product_slug>/" , views.product_details , name="product_details"),
]
