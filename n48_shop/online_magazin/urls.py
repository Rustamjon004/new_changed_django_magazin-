from django.urls import path
from online_magazin import views
urlpatterns = [
    path('index/',  views.product_list, name='product_list'),
    path('category/<int:category_id>/views.product_list', views.product_list, name='category_detail_id'),
    path('product-detail/<int:product_id>/',views.product_detail,name='product_detail')
]