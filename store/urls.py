from django.urls import path

from . import views


urlpatterns = [
    path('',views.category,name='category'),
    path('category/<slug:category_slug>/',views.category,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_details,name='product_details'),


    path('search/',views.search,name='search'), 
]