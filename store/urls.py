from django.urls import path
from . import views

urlpatterns = [
    path("" , views.store , name="store"),
    path("sub_category/<slug:sub_category_slug>/" , views.store , name="sub_category"),
    path("sub_category/<slug:sub_category_slug>/<slug:product_slug>/" , views.product_details , name="product_details"),
    path("search/" , views.search , name='search'),
]
