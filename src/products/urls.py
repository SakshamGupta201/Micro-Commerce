from django.urls import path
from .views import product_create_view, product_detail_view, product_list_view

urlpatterns = [
    path("", product_list_view, name="product-list"),
    path("create/", product_create_view, name="product-create"),
    path("<slug:handle>/", product_detail_view, name="product-detail"),
]
